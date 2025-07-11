# main.py
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles

from src.config import BASE_DIR
from src.models import FullPayload
from src.routers import b50, table

router = APIRouter()
app = FastAPI()

# 挂载静态文件
app.mount("/static_mai_b50", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# 包含路由
app.include_router(b50.router)
app.include_router(table.router)

# 共享全局状态
app.state.POST_DATA = None

@app.post("/")
async def _(data: FullPayload):
    app.state.POST_DATA = data
    return {"status": "ok"}

# 启动代码
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=13004, reload=True)