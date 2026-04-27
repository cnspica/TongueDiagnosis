import requests
import json
from starlette.responses import JSONResponse, StreamingResponse
from ..orm import create_new_chat_records, get_chat_record
from ..orm.database import SessionLocal
from ..config import settings


class OllamaStreamChatter:
    def __init__(self, model=settings.LLM_NAME,
                 system_prompt=None
                 ):
        self.backend = settings.LLM_BACKEND  # "ollama" 或 "openai_compatible"
        self.url = settings.OLLAMA_PATH
        self.headers = {"Content-Type": "application/json"}
        self.messages = []
        self.model = model

        # OpenAI 兼容配置
        if self.backend == "openai_compatible":
            self.openai_base = settings.OPENAI_API_BASE.rstrip("/")
            self.openai_url = f"{self.openai_base}/chat/completions"
            self.openai_key = settings.OPENAI_API_KEY
            self.openai_model = settings.OPENAI_MODEL
            self.headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.openai_key}"
            }

        if system_prompt:
            self.messages.append({
                "role": "system",
                "content": system_prompt
            })

    def chat_stream_first(self, user_input, feature, id, db, session_new_id, cropped_img_src=None):
        self.messages = []
        self.messages.append({"role": "user", "content": "用户的舌部特征为：" + feature + "。" + user_input + "。请用中文回答。"})

        if self.backend == "openai_compatible":
            return self._chat_stream_openai(self.messages, db, session_new_id, cropped_img_src)
        else:
            return self._chat_stream_ollama(self.messages, db, session_new_id, cropped_img_src)

    def chat_stream_add(self, id, db, session_id):
        chat_record = get_chat_record(ID=id, sessionid=session_id, db=db)
        records = []
        for record in chat_record:
            role = "user" if record.role == 1 else "assistant"
            records.append({"role": role, "content": record.content})
        self.messages = records

        if self.backend == "openai_compatible":
            return self._chat_stream_openai(self.messages, db, session_id)
        else:
            return self._chat_stream_ollama(self.messages, db, session_id)

    # ===== OpenAI 兼容 API 流式 =====
    def _chat_stream_openai(self, messages, db, session_id, cropped_img_src=None):
        data = {
            "model": self.openai_model,
            "messages": messages,
            "stream": True
        }
        try:
            print(f"[LLM-OPENAI] POST {self.openai_url}, model={self.openai_model}")
            response = requests.post(
                self.openai_url,
                headers=self.headers,
                json=data,
                stream=True,
                timeout=120
            )
            response.raise_for_status()

            def generate():
                full_response = ""
                # 首先发送裁剪图片路径
                if cropped_img_src:
                    yield json.dumps({
                        "token": "",
                        "session_id": session_id,
                        "is_complete": False,
                        "cropped_img_src": cropped_img_src
                    }) + "\n"

                for line in response.iter_lines():
                    if not line:
                        continue
                    line_str = line.decode('utf-8').strip()
                    # SSE 格式: "data: {...}" 或 "data: [DONE]"
                    if line_str.startswith("data: "):
                        payload = line_str[6:]
                        if payload.strip() == "[DONE]":
                            break
                        try:
                            chunk = json.loads(payload)
                            choices = chunk.get("choices", [])
                            if not choices:
                                continue
                            delta = choices[0].get("delta", {})
                            # 跳过思维链内容（reasoning_content），只取正文
                            content = delta.get("content", "")
                            if content:
                                full_response += content
                                yield json.dumps({
                                    "token": content,
                                    "session_id": session_id,
                                    "is_complete": False
                                }) + "\n"
                        except json.JSONDecodeError:
                            print(f"[LLM-OPENAI] Failed to parse SSE payload: {payload[:100]}")
                            continue

                yield json.dumps({
                    "token": full_response,
                    "session_id": session_id,
                    "is_complete": True
                }) + "\n"
                self._save_to_db_async(db, full_response, session_id)

            return StreamingResponse(
                generate(),
                media_type='application/x-ndjson'
            )
        except requests.exceptions.RequestException as e:
            print(f"[LLM-OPENAI] Request failed: {e}")
            return JSONResponse(
                status_code=500,
                content={"error": f"线上模型请求失败: {str(e)}"}
            )

    # ===== Ollama 本地模型流式 =====
    def _chat_stream_ollama(self, messages, db, session_id, cropped_img_src=None):
        data = {
            "model": self.model,
            "messages": messages,
            "stream": True
        }
        try:
            print(f"[LLM-OLLAMA] POST {self.url}, model={self.model}")
            response = requests.post(
                self.url,
                headers={"Content-Type": "application/json"},
                json=data,
                stream=True
            )
            response.raise_for_status()

            def generate():
                full_response = ""
                # 首先发送裁剪图片路径
                if cropped_img_src:
                    yield json.dumps({
                        "token": "",
                        "session_id": session_id,
                        "is_complete": False,
                        "cropped_img_src": cropped_img_src
                    }) + "\n"
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line.decode('utf-8'))
                        if 'message' in chunk:
                            content = chunk['message']['content']
                            full_response += content
                            yield json.dumps({
                                "token": content,
                                "session_id": session_id,
                                "is_complete": False
                            }) + "\n"
                yield json.dumps({
                    "token": full_response,
                    "session_id": session_id,
                    "is_complete": True
                }) + "\n"
                self._save_to_db_async(db, full_response, session_id)

            return StreamingResponse(
                generate(),
                media_type='application/x-ndjson'
            )
        except requests.exceptions.RequestException as e:
            print(f"[LLM-OLLAMA] Request failed: {e}")
            return JSONResponse(
                status_code=500,
                content={"error": f"Ollama请求失败: {str(e)}"}
            )

    def _save_to_db_async(self, db, content, session_id):
        import asyncio
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = None

        def save_task():
            try:
                local_db = SessionLocal()
                try:
                    create_new_chat_records(
                        db=local_db,
                        content=content,
                        session_id=session_id,
                        role=2
                    )
                    local_db.commit()
                except Exception as e:
                    local_db.rollback()
                    print(f"数据库保存失败: {e}")
                finally:
                    local_db.close()
            except Exception as e:
                print(f"数据库会话创建失败: {e}")

        # 使用独立 DB Session 在新线程中执行，避免线程安全问题
        import threading
        threading.Thread(target=save_task, daemon=True).start()
