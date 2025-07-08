from pydantic import BaseModel
from typing import Dict, Any
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

# --- 初始化 ---

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static_mai_b50", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

last_post_data = None

# --- 模型定义 ---

class Score(BaseModel):
    scores: Dict[str, Any]

class User(BaseModel):
    username: str
    nameplate: str
    icon: str

class FullPayload(BaseModel):
    user: User
    score: Score

# --- 工具函数 ---

def get_difficulty_class(level_index: int) -> str:
    return ['basic', 'advanced', 'expert', 'master', 'remaster'][level_index] if 0 <= level_index < 5 else 'basic'

def get_fc_image(fc: int) -> str:
    return {
        3: 'UI_MSS_MBase_Icon_FC.png',
        2: 'UI_MSS_MBase_Icon_FCp.png',
        1: 'UI_MSS_MBase_Icon_AP.png',
        0: 'UI_MSS_MBase_Icon_APp.png'
    }.get(fc, '')

def get_fs_image(fs: int) -> str:
    return {
        0: 'UI_MSS_MBase_Icon_Sync.png',
        1: 'UI_MSS_MBase_Icon_FS.png',
        2: 'UI_MSS_MBase_Icon_FSp.png',
        3: 'UI_MSS_MBase_Icon_FSD.png',
        4: 'UI_MSS_MBase_Icon_FSDp.png'
    }.get(fs, '')

def get_dxstars_image(dx_score: int, total_dx_score: int) -> str:
    if total_dx_score == 0:
        return ''
    percentage = (dx_score / total_dx_score) * 100
    if percentage < 85:
        return ''
    elif percentage < 90:
        return "UI_GAM_Gauge_DXScoreIcon_01.png"
    elif percentage < 93:
        return "UI_GAM_Gauge_DXScoreIcon_02.png"
    elif percentage < 95:
        return "UI_GAM_Gauge_DXScoreIcon_03.png"
    elif percentage < 97:
        return "UI_GAM_Gauge_DXScoreIcon_04.png"
    else:
        return "UI_GAM_Gauge_DXScoreIcon_05.png"

def get_rating_img(rating: int) -> str:
    thresholds = [15000, 14500, 14000, 13000, 12000, 10000, 7000, 4000, 2000, 1000, 0]
    filenames = [
        "UI_CMN_DXRating_11.png", "UI_CMN_DXRating_10.png", "UI_CMN_DXRating_09.png",
        "UI_CMN_DXRating_08.png", "UI_CMN_DXRating_07.png", "UI_CMN_DXRating_06.png",
        "UI_CMN_DXRating_05.png", "UI_CMN_DXRating_04.png", "UI_CMN_DXRating_03.png",
        "UI_CMN_DXRating_02.png", "UI_CMN_DXRating_01.png"
    ]
    for threshold, filename in zip(thresholds, filenames):
        if rating >= threshold:
            return filename
    return filenames[-1]

def pad_scores(data: FullPayload) -> FullPayload:
    for key, target_len in [("scores_b35", 35), ("scores_b15", 15)]:
        original = data.score.scores.get(key, [])
        data.score.scores[key] = list(original)[:target_len] + [{}] * (target_len - len(original))
    return data

# --- 路由 ---

@app.post("/b50")
async def receive_scores(data: FullPayload):
    global last_post_data
    last_post_data = pad_scores(data)
    return {"status": "ok"}

@app.get("/b50", response_class=HTMLResponse)
async def render_scores(request: Request):
    if not last_post_data:
        return HTMLResponse("<h1>无数据</h1>", status_code=404)

    user = last_post_data.user
    score = last_post_data.score

    return templates.TemplateResponse("b50.html", {
        "request": request,
        "user_data": {
            "username": user.username,
            "icon_img": user.icon,
            "nameplate": user.nameplate,
            "rating_img": get_rating_img(score.scores.get("rating", 0))
        },
        "score_data": {
            "scores": score.scores
        },
        "get_difficulty_class": get_difficulty_class,
        "get_fc_image": get_fc_image,
        "get_fs_image": get_fs_image,
        "get_dxstars_image": get_dxstars_image,
    })

# --- 启动 ---

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=13003, reload=True)
