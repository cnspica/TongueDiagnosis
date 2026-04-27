import bcrypt
from sqlalchemy.orm import Session
from ...models import models

def _hash_password(password: str) -> str:
    """使用 bcrypt 加盐哈希密码"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def _verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码是否匹配"""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def register_user(email: str, password: str, db: Session):
    password = _hash_password(password)
    user = models.User(
        email=email,
        password=password
    )
    if db.query(models.User).filter(models.User.email == email).first():
        return 101
    db.add(user)
    try:
        db.commit()
        return 0
    except Exception as error:
        db.rollback()
        print(error)
        return 102

def login_user(email: str, password: str, db: Session):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        if _verify_password(password, user.password):
            return 0
        else:
            return 102  # 密码不匹配
    else:
        return 101  # 用户不存在

def get_user(email: str, db: Session):
    return db.query(models.User).filter(models.User.email == email).first()


def authenticate_user(email: str, password: str, db: Session):
    user = get_user(email=email, db=db)
    if not user:
        return False
    if not _verify_password(password, user.password):
        return False
    return user

def get_user_record(ID: int, db: Session):
    return db.query(models.TongueAnalysis).filter(models.TongueAnalysis.user_id == ID).all()
