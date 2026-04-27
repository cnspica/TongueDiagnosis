import os
import secrets
from dotenv import load_dotenv

# 自动加载项目根目录的 .env 文件（本地开发使用）
load_dotenv()

class Settings:
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    # 优先使用环境变量，否则自动生成安全密钥（生产环境务必设置环境变量）
    SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY", secrets.token_hex(32))
    ALGORITHMS: str = "HS256"
    IMG_PATH: str = "frontend/public/tongue"
    IMG_DB_PATH: str = "tongue"

    # ===== LLM 后端配置 =====
    # 可选值: "ollama" 或 "openai_compatible"
    LLM_BACKEND: str = os.environ.get("LLM_BACKEND", "openai_compatible")

    # Ollama 本地模型配置
    OLLAMA_PATH: str = os.environ.get("OLLAMA_PATH", "http://localhost:11434/api/chat")
    LLM_NAME: str = os.environ.get("LLM_NAME", "qwen3:8b")

    # OpenAI 兼容 API 配置（阶跃星辰 StepFun 等）
    # ⚠️ API Key 必须通过环境变量或 .env 文件配置，切勿硬编码在代码中
    OPENAI_API_BASE: str = os.environ.get("OPENAI_API_BASE", "https://chatapi.stepfun.com/chatapi/v1")
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")  # 必须在 .env 中设置
    OPENAI_MODEL: str = os.environ.get("OPENAI_MODEL", "step-3.5-flash")

    SYSTEM_PROMPT: str = "你现在是一位专注于舌诊的中医AI医生。我会首先向你展示用户舌头的四项图像特征，请运用你的中医知识为用户提供调理建议。请用中文回答。"
    APP_PORT: int = int(os.environ.get("APP_PORT", "5000"))
