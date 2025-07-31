# main.py
import json

from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from src.config import BASE_DIR
from src.models import FullPayload
from src.routers import b50, table, scores_list, music_data

router = APIRouter()
app = FastAPI()

# 挂载静态文件
app.mount("/static_mai_b50", StaticFiles(directory=str(BASE_DIR / "src" / "web" / "static")), name="static")

# 包含路由
app.include_router(b50.router)
app.include_router(table.router)
app.include_router(scores_list.router)
app.include_router(music_data.router)

# 共享全局状态
app.state.POST_DATA = None

data_dir = Path(__file__).parent / "client_data"
with open(data_dir / "all.json", "r", encoding="utf-8") as f:
    analysis_raw_data = json.load(f)

# 确保 song_id 是 int 类型（与主数据一致），构建索引映射
flat_list = []
for item in analysis_raw_data:
    flat_list.append({
        "song_id": int(item["song_id"]),
        "difficulty_index": item["difficulty_index"],
        "special_breaks": item["special_breaks"],
        "chart_type": item["chart_type"]
    })

app.state.ANALYSIS_DATA = flat_list

@app.post("/")
async def _(data: FullPayload):
    app.state.POST_DATA = data
    return {"status": "ok"}

# 启动代码
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=13004, reload=True)