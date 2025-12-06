# app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 创建FastAPI应用
app = FastAPI(
    title="iCoursera API",
    description="AI在线教育平台API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "*"  # 开发阶段允许所有
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 主页
@app.get("/")
def read_root():
    return {
        "message": "欢迎使用 iCoursera API",
        "status": "运行中",
        "docs": "/docs",
        "endpoints": {
            "热门课程": "/api/courses/hot",
            "课程列表": "/api/courses",
            "课程分类": "/api/categories",
            "用户登录": "/api/auth/login",
            "用户注册": "/api/auth/register"
        }
    }

# 健康检查
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# 🔧 关键：导入并包含路由
from api import courses, auth
app.include_router(courses.router)
app.include_router(auth.router)

if __name__ == "__main__":
    import uvicorn
    print("🚀 启动 iCoursera API 服务...")
    print("📚 文档地址: http://localhost:8000/docs")
    print("🌐 API地址: http://localhost:8000")
    print("=" * 50)
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)