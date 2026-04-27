import os
import time
import asyncio
from fastapi import APIRouter, Depends, UploadFile, Body, Form, File, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from tempfile import SpooledTemporaryFile
from .ollama_used import OllamaStreamChatter
from ..core import get_current_user
from ..models import schemas
from ..orm.database import get_db
from ..orm import write_event, write_result, get_record_by_location, get_chat_record, get_all_chat_id, get_result, create_new_session, create_new_chat_records
from ..config import Settings
from ..net.predict import TonguePredictor
from ..config import settings

# 允许的图片类型和最大文件大小（10MB）
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

router_tongue_analysis = APIRouter()

feature_map = {
    "舌色": {
        0: "淡白舌",
        1: "淡红舌",
        2: "红舌",
        3: "绛舌",
        4: "青紫舌"
    },
    "舌苔颜色": {
        0: "白苔",
        1: "黄苔",
        2: "灰黑苔"
    },
    "舌体厚薄": {
        0: "薄",
        1: "厚"
    },
    "舌体腐腻": {
        0: "腐",
        1: "腻"
    }
}

def format_tongue_features(tongue_color,
                           coating_color,
                           tongue_thickness,
                           rot_greasy):
    try:
        features = [
            f"舌色: {feature_map['舌色'][tongue_color]}",
            f"舌苔颜色: {feature_map['舌苔颜色'][coating_color]}",
            f"舌体厚薄: {feature_map['舌体厚薄'][tongue_thickness]}",
            f"舌体腐腻: {feature_map['舌体腐腻'][rot_greasy]}"
        ]
        return "，".join(features)
    except KeyError as e:
        missing_key = int(str(e).split("'")[1])
        return f"错误：检测到无效特征值 {missing_key}，请检查输入范围"


class UserInput(BaseModel):
    input: str

@router_tongue_analysis.post('/session/{sessionId}')
async def upload(sessionId: int,
                 user_input: UserInput,
                 user: schemas.UserBase = Depends(get_current_user),
                 db: Session = Depends(get_db),
                 ):
    if not user:
        return schemas.BaseResponse(
            code=101,
            message="can not find user",
            data=None
        )
    else:
        bot = OllamaStreamChatter(
            system_prompt=settings.SYSTEM_PROMPT
        )
        create_new_chat_records(db=db, content=user_input.input, session_id=sessionId, role=1)
        return bot.chat_stream_add(user.id, db, sessionId)


class inputPicture(BaseModel):
    file_data: UploadFile
    user_input: str
    name: str

@router_tongue_analysis.post('/session')
async def upload(file_data: UploadFile = File(...),
                user_input: str = Form(...),
                name: str = Form(...),
                 user: schemas.UserBase = Depends(get_current_user),
                 db: Session = Depends(get_db)
                 ):
    if not user:
        return schemas.BaseResponse(
            code=101,
            message="can not find user",
            data=None
        )

    try:
        # 文件类型校验
        file_ext = os.path.splitext(file_data.filename)[1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=f"不支持的文件类型: {file_ext}，仅支持 {', '.join(ALLOWED_EXTENSIONS)}")

        # 文件大小校验
        contents = await file_data.read()
        print(f"[DEBUG] File received: {file_data.filename}, size={len(contents)} bytes, ext={file_ext}")
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail=f"文件大小超过限制（最大 {MAX_FILE_SIZE // (1024*1024)}MB）")
        await file_data.seek(0)

        def analysis(img: SpooledTemporaryFile, record_id: int, function, img_save_path: str = None):
            predictor = TonguePredictor()
            predictor.predict(img=img, record_id=record_id, fun=function, img_save_path=img_save_path)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = os.path.splitext(file_data.filename)[1]
        filename = f"{timestamp}{file_extension}"
        file_location = f"{Settings.IMG_PATH}/{filename}"
        with open(file_location, "wb") as f:
            contents = await file_data.read()
            f.write(contents)
        print(f"[DEBUG] File saved to: {file_location}")

        # 重置文件指针，确保后续 predictor.predict 能正确读取
        await file_data.seek(0)

        img_db_path = f"{Settings.IMG_DB_PATH}/{filename}"
        code = write_event(user_id=user.id, img_src=img_db_path, state=0, db=db)
        print(f"[DEBUG] write_event code={code}, img_db_path={img_db_path}")

        if code == 0:
            record = get_record_by_location(img_db_path, db=db)
            print(f"[DEBUG] record id={record.id}, state={record.state}")
            analysis(img=file_data.file, record_id=record.id, function=write_result, img_save_path=file_location)
            print(f"[DEBUG] analysis called, waiting for result...")
            wait_count = 0
            while True:
                result1 = get_result(img_db_path, db=db)
                print(f"[DEBUG] Polling result: state={result1.state}, count={wait_count}")
                if result1.state != 0:
                    break
                wait_count += 1
                if wait_count > 120:  # 最多等120秒
                    return schemas.BaseResponse(code=500, message="AI推理超时", data=None)
                await asyncio.sleep(1)

            result = get_result(img_db_path, db=db)
            print(f"[DEBUG] Final result: state={result.state}, tongue_color={result.tongue_color}")
            if result.state != 1:
                return schemas.BaseResponse(
                    code=result.state,
                    message="图片有问题",
                    data=None
                )
            tongue_color = result.tongue_color
            coating_color = result.coating_color
            tongue_thickness = result.tongue_thickness
            rot_greasy = result.rot_greasy
            cropped_img_src = result.cropped_img_src
            feature = format_tongue_features(tongue_color,coating_color,tongue_thickness,rot_greasy)
            print(f"[DEBUG] Feature: {feature}, cropped_img_src: {cropped_img_src}")
            bot = OllamaStreamChatter(
                system_prompt=settings.SYSTEM_PROMPT
            )
            new_message = create_new_session(ID=user.id, db=db, tittle=name)
            session_new_id = new_message.id
            create_new_chat_records(db=db, content=user_input, session_id=session_new_id, role=1)
            print(f"[DEBUG] Starting LLM stream, session_id={session_new_id}")
            return bot.chat_stream_first(user_input, feature, user.id, db, session_new_id, cropped_img_src=cropped_img_src)
        else:
            return schemas.UploadResponse(
                code=201,
                message="operation failed",
                data=None
            )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Diagnosis failed: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"诊断失败: {str(e)}")

@router_tongue_analysis.get("/record/{sessionid}", response_model=schemas.ChatSessionRecordsResponse)
async def get_chat_records_by_session(sessionid: int,
                                      db: Session = Depends(get_db),
                                      user: schemas.UserBase = Depends(get_current_user)
                                      ):
    if not user:
        return schemas.ChatSessionRecordsResponse(
            code=101,
            message="can not find user",
            data={"records": []}
        )
    else:
        chat_record = get_chat_record(ID=user.id, sessionid=sessionid, db=db)
        if chat_record == 102 or chat_record == 103:
            return schemas.ChatSessionRecordsResponse(
                code=chat_record,
                message="operation failed",
                data={"records": []}
            )
        else:
            records = []
            for record in chat_record:
                records.append(schemas.ChatRecordResponse(
                    content=record.content,
                    create_at=record.create_at,
                    role=record.role
                ))
            data_temp = {
                "records": records
            }
            return schemas.ChatSessionRecordsResponse(
                code=0,
                message="operation success",
                data=data_temp,
            )

@router_tongue_analysis.get("/session", response_model=schemas.SessionIdResponse)
async def get_chat_records_id(db: Session = Depends(get_db),
                              user: schemas.UserBase = Depends(get_current_user)):
    if not user:
        return schemas.SessionIdResponse(
            code=101,
            message="can not find user",
            data=[]
        )
    else:
        chat_id_records = get_all_chat_id(ID=user.id, db=db)
        data_temp = []
        for record in chat_id_records:
            data_temp.append(schemas.SessionId(
                session_id=record.id,
                name=record.tittle
            ))
        return schemas.SessionIdResponse(
            code=0,
            message="operation success",
            data=data_temp
        )
