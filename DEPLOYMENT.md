# 中医舌诊 AI 系统部署文档

> 版本：v1.0 | 更新日期：2026-04-22

---

## 目录

1. [系统架构概览](#1-系统架构概览)
2. [环境要求](#2-环境要求)
3. [后端部署](#3-后端部署)
4. [前端部署](#4-前端部署)
5. [AI 模型部署](#5-ai-模型部署)
6. [环境变量配置](#6-环境变量配置)
7. [Nginx 生产部署](#7-nginx-生产部署)
8. [数据库迁移注意事项](#8-数据库迁移注意事项)
9. [常见问题排查](#9-常见问题排查)

---

## 1. 系统架构概览

```
┌─────────────────────────────────────────────────────┐
│                    Nginx (80/443)                    │
│              反向代理 + 静态文件服务                    │
└──────────────┬──────────────────┬───────────────────┘
               │                  │
       /api/*  │                  │  /*
               ▼                  ▼
┌──────────────────────┐  ┌───────────────────────┐
│   FastAPI 后端        │  │   Vue 前端 (dist)      │
│   localhost:5000      │  │   静态文件              │
└──────┬───────────────┘  └───────────────────────┘
       │
       ├── SQLite 数据库
       ├── Ollama (localhost:11434)
       ├── YOLOv5 舌体检测
       ├── SAM 分割
       └── ResNet50 特征分类
```

**技术栈：**
- 前端：Vue 3 + Vite + Element Plus + Pinia + MarkdownIt
- 后端：FastAPI + SQLAlchemy + SQLite + JWT
- AI：YOLOv5 + SAM + ResNet50 + Ollama (Qwen3:32b)

---

## 2. 环境要求

| 项目 | 最低要求 | 推荐配置 |
|------|---------|---------|
| Python | 3.9+ | 3.11 |
| Node.js | 18+ | 20 LTS |
| CUDA | 11.8+ (GPU) | 12.1+ |
| 内存 | 8 GB | 16 GB+ |
| 显存 | 4 GB | 8 GB+ (模型推理) |
| 磁盘 | 10 GB | 20 GB+ (含模型权重) |

---

## 3. 后端部署

### 3.1 克隆项目

```bash
git clone <repo-url> TongueDiagnosis
cd TongueDiagnosis
```

### 3.2 创建虚拟环境

```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 3.3 安装依赖

```bash
pip install -r requirements.txt
pip install bcrypt  # 密码加密（新增依赖）
```

### 3.4 配置环境变量

创建 `.env` 文件（项目根目录）：

```env
# JWT 密钥（生产环境必须设置！不设置则每次重启自动生成，导致已登录用户失效）
JWT_SECRET_KEY=your-secure-random-key-at-least-64-chars

# Ollama 服务地址
OLLAMA_PATH=http://localhost:11434/api/chat

# LLM 模型名称
LLM_NAME=qwen3:32b

# 后端端口
APP_PORT=5000

# CORS 允许的前端域名（逗号分隔）
CORS_ORIGINS=http://your-domain.com,https://your-domain.com
```

> ⚠️ **重要**：`JWT_SECRET_KEY` 在生产环境必须手动设置！否则每次重启后端，所有用户的 Token 会失效。

### 3.5 初始化数据库

```bash
# 首次运行会自动创建 SQLite 数据库
python run.py
```

数据库文件默认位于 `instance/tongue_diagnosis.db`。

### 3.6 启动服务

```bash
# 开发环境
python run.py

# 生产环境（使用 uvicorn）
uvicorn application:app --host 0.0.0.0 --port 5000 --workers 1
```

> 注意：由于使用了单例模型预测队列，workers 只能为 1。

---

## 4. 前端部署

### 4.1 安装依赖

```bash
cd frontend
npm install
```

### 4.2 配置环境变量

编辑 `frontend/.env`：

```env
# 开发环境
VITE_API_URL=http://localhost:5000
```

编辑 `frontend/.env.production`：

```env
# 生产环境
VITE_API_URL=http://your-server:5000
# 或使用 Nginx 代理时写相对路径
# VITE_API_URL=
```

### 4.3 开发模式

```bash
npm run dev
# 访问 http://localhost:5173
```

### 4.4 构建生产版本

```bash
npm run build
# 输出到 frontend/dist/
```

---

## 5. AI 模型部署

### 5.1 安装 Ollama

```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# 从 https://ollama.com/download 下载安装
```

### 5.2 拉取模型

```bash
ollama pull qwen3:32b
```

### 5.3 启动 Ollama 服务

```bash
# 默认运行在 http://localhost:11434
ollama serve
```

### 5.4 YOLOv5 / SAM / ResNet50 权重

将预训练权重文件放置到 `application/net/weights/` 目录下：

```
application/net/weights/
├── tongue_detect.pt      # YOLOv5 舌体检测
├── tongue_segment.pt     # SAM 分割
└── tongue_classify.pt    # ResNet50 分类
```

---

## 6. 环境变量配置

### 后端环境变量一览

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `JWT_SECRET_KEY` | 自动生成 | JWT 签名密钥，生产必须设置 |
| `OLLAMA_PATH` | `http://localhost:11434/api/chat` | Ollama API 地址 |
| `LLM_NAME` | `qwen3:32b` | 使用的 LLM 模型 |
| `APP_PORT` | `5000` | 后端监听端口 |
| `CORS_ORIGINS` | `http://127.0.0.1:5173,http://localhost:5173` | 允许的前端域名 |

### 前端环境变量一览

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `VITE_API_URL` | `http://localhost:5000` | 后端 API 地址 |

---

## 7. Nginx 生产部署

### 7.1 Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /path/to/TongueDiagnosis/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API 代理
    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 流式响应支持
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 300s;
    }

    # 舌诊图片静态文件
    location /tongue/ {
        alias /path/to/TongueDiagnosis/frontend/public/tongue/;
        expires 30d;
    }

    client_max_body_size 10m;  # 匹配后端 MAX_FILE_SIZE
}
```

### 7.2 HTTPS 配置（推荐）

```bash
# 使用 certbot 获取 Let's Encrypt 证书
sudo certbot --nginx -d your-domain.com
```

---

## 8. 数据库迁移注意事项

### 8.1 从旧版升级（SHA-256 → bcrypt）

由于密码加密方式从 SHA-256 变更为 bcrypt，**旧用户密码将无法验证**。需要执行以下操作之一：

**方案 A：重置所有密码（简单）**

```python
# 进入 Python Shell
from application.orm.database import SessionLocal
from application.models.models import User
from application.orm.crud.auth_user import _hash_password

db = SessionLocal()
users = db.query(User).all()
for user in users:
    # 将旧 SHA-256 哈希标记为需要重置
    user.password = _hash_password("default_password_123")
    print(f"User {user.email} password reset to default_password_123")
db.commit()
db.close()
```

**方案 B：添加迁移脚本兼容旧密码**

在 `auth_user.py` 中添加兼容逻辑：

```python
import hashlib

def _verify_password_legacy(plain_password: str, hashed_password: str) -> bool:
    """兼容旧的 SHA-256 密码"""
    sha256_hash = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
    return sha256_hash == hashed_password

def login_user(email: str, password: str, db: Session):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return 101
    # 先尝试 bcrypt
    if _verify_password(password, user.password):
        return 0
    # 再尝试旧的 SHA-256
    if _verify_password_legacy(password, user.password):
        # 登录成功后自动升级为 bcrypt
        user.password = _hash_password(password)
        db.commit()
        return 0
    return 102
```

### 8.2 Email 唯一约束

新版为 `User.email` 添加了 `unique=True` 和 `index=True`。如果已有数据库包含重复 email，需要先清理：

```python
from application.orm.database import SessionLocal
from application.models.models import User
from sqlalchemy import func

db = SessionLocal()
# 查找重复 email
duplicates = db.query(User.email, func.count(User.email))\
    .group_by(User.email)\
    .having(func.count(User.email) > 1)\
    .all()
for email, count in duplicates:
    print(f"重复 email: {email} ({count}条)")
db.close()
```

清理后删除旧数据库文件重新创建，或手动添加唯一约束：

```sql
CREATE UNIQUE INDEX ix_user_email ON "User" (email);
```

---

## 9. 常见问题排查

### Q1: 启动后端报错 `ModuleNotFoundError: No module named 'bcrypt'`

```bash
pip install bcrypt
# 或在 venv 中
.\venv\Scripts\pip install bcrypt
```

### Q2: 前端构建报错 `ModuleNotFoundError: No module named 'dompurify'`

```bash
cd frontend
npm install dompurify
```

### Q3: 登录失败，返回 401

- 检查 `JWT_SECRET_KEY` 是否在重启后变了
- 确认后端登录接口已从 `PUT` 改为 `POST`
- 清除浏览器 localStorage 中的旧 Token

### Q4: 上传舌诊图片返回 400

- 确认图片格式为 `.jpg/.jpeg/.png/.bmp/.webp`
- 文件大小不超过 10MB

### Q5: AI 回复为空或报错

- 确认 Ollama 服务正在运行：`curl http://localhost:11434/api/tags`
- 确认模型已拉取：`ollama list`
- 检查 `OLLAMA_PATH` 环境变量配置

### Q6: 流式响应中断

- Nginx 配置需关闭 `proxy_buffering`
- 检查 `proxy_read_timeout` 设置是否足够（推荐 300s）

### Q7: 旧用户登录密码错误

- 密码已从 SHA-256 升级为 bcrypt，参考 [8.1 节](#81-从旧版升级sha-256--bcrypt) 执行迁移

---

## 附录：修复清单

本次部署文档对应的代码修复清单：

| 优先级 | 编号 | 修复内容 | 涉及文件 |
|--------|------|---------|---------|
| 🔴 P0 | S5 | v-html XSS → DOMPurify 净化 | `main.vue` |
| 🔴 P0 | S3 | 文件上传类型/大小校验 | `model_api.py` |
| 🔴 P0 | B5 | async 阻塞 → asyncio.sleep | `model_api.py` |
| 🟠 P1 | B1+B2 | slide_tip 非响应式 + 动画无效 | `Register_Login.vue` |
| 🟠 P1 | B3 | 上传组件竞态条件 | `UploadPicture.vue` |
| 🟠 P1 | B7 | 密码字段引用错误 | `auth_user.py` |
| 🟠 P1 | S1 | JWT 密钥改环境变量 | `config.py` |
| 🟡 P2 | S4 | CORS 移除通配符 | `__init__.py` |
| 🟡 P2 | S2 | SHA-256 → bcrypt 加盐 | `auth_user.py` |
| 🟡 P2 | M1 | 登录 PUT → POST | `user_api.py` + `Loginblock.vue` |
| 🟡 P2 | M2 | ServerUrl 改环境变量 | `config.js` + `.env` |
| 🟡 P2 | M5 | AI 提示词统一中文 | `model_api.py` + `ollama_used.py` |
| 🟡 P2 | M7 | email 添加唯一约束 | `models.py` |
| 🟡 P2 | B6 | 密码允许特殊字符 | `Registerblock.vue` + `Loginblock.vue` |
| 🟢 P3 | M4 | 清理未使用文件 | `counter.js`, `WelcomeItem.vue`, `icons/` |
| 🟢 P3 | M10 | 移除 vuex | `package.json` |
| 🟢 P3 | M9 | datetime.utcnow → now(timezone.utc) | `authentication.py` |
| 🟢 P3 | M3 | Vite 绑定 localhost | `vite.config.js` |
| 🟢 P3 | B4 | DB Session 线程安全 | `ollama_used.py` |
