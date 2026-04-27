import os
from sqlalchemy.orm import Session
from application.models import models
from ..database import get_db_object
from ...config import Settings

def write_result(
        event_id: int,
        tongue_color: int,
        coating_color: int,
        tongue_thickness: int,
        rot_greasy: int,
        code: int,
        cropped_img_path: str = None,
        db: Session = get_db_object()
):
    record = db.query(models.TongueAnalysis).filter(models.TongueAnalysis.id == event_id).first()
    if code == 1:
        if record:
            record.tongue_color = tongue_color
            record.coating_color = coating_color
            record.tongue_thickness = tongue_thickness
            record.rot_greasy = rot_greasy
            record.state = code
            # 保存抠图路径到数据库（转换为相对路径）
            if cropped_img_path:
                try:
                    # cropped_img_path 形如 "frontend/public/tongue/xxx_crop.jpg"
                    # 需要转换为 "tongue/xxx_crop.jpg"（去掉 frontend/public/ 前缀）
                    path_normalized = cropped_img_path.replace("\\", "/")
                    img_dir = Settings.IMG_PATH.replace("\\", "/")
                    if path_normalized.startswith(img_dir):
                        cropped_img_src = Settings.IMG_DB_PATH + path_normalized[len(img_dir):]
                    else:
                        # 尝试从文件名提取
                        cropped_img_src = Settings.IMG_DB_PATH + "/" + os.path.basename(cropped_img_path)
                    record.cropped_img_src = cropped_img_src
                    print(f"[CROP] Saved cropped_img_src to DB: {cropped_img_src}")
                except Exception as e:
                    print(f"[CROP] Failed to save cropped_img_src: {e}")
            try:
                db.commit()
                return 0
            except Exception as error:
                db.rollback()
                print(error)
                return 1
        return None
    else:
        record.state = code
        try:
            db.commit()
            return 0
        except Exception as error:
            db.rollback()
            print(error)
            return 1

def write_event(
    user_id: int,
    img_src: str,
    state: int,
    db: Session
):
    event = models.TongueAnalysis(
        user_id=user_id,
        img_src=img_src,
        state=state,
    )
    db.add(event)
    try:
        db.commit()
        return 0
    except Exception as error:
        db.rollback()
        print(error)
        return 201


def get_record_by_location(
    img_src: str,
    db: Session
):
    return db.query(models.TongueAnalysis).filter(models.TongueAnalysis.img_src == img_src).first()
