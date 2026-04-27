from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import register_routes
import os

def create_app():
    app = FastAPI()
    # 从环境变量读取允许的前端域名，逗号分隔
    default_origins = "http://127.0.0.1:5173,http://localhost:5173"
    origins_str = os.environ.get("CORS_ORIGINS", default_origins)
    origins = [o.strip() for o in origins_str.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_routes(app)
    return app
