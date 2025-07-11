# routers/b50.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..config import BASE_DIR, MUSIC_DATA
from ..utils import get_rating_img, pad_b50, get_difficulty_class, get_fc_image, get_fs_image, get_dxstars_image

router = APIRouter()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@router.get("/b50", response_class=HTMLResponse)
async def _(request: Request):
    POST_DATA = request.app.state.POST_DATA
    if not POST_DATA:
        return HTMLResponse("<h1>无数据</h1>", status_code=404)
    
    user_data = POST_DATA.user_data
    # 分数来源是 bests 还是 scores，前者直接用，后者要转换（后者可以进行筛选，例如ap50、fdx50等）
    if POST_DATA.scores_b50_data:
        rating = POST_DATA.scores_b50_data["rating"]
        rating_b35 = POST_DATA.scores_b50_data["rating_b35"]
        rating_b15 = POST_DATA.scores_b50_data["rating_b15"]
        scores_b35 = POST_DATA.scores_b50_data["scores_b35"]
        scores_b15 = POST_DATA.scores_b50_data["scores_b15"]
    else:
        score = POST_DATA.scores_data
        # 可以进行筛选，例如ap50、fdx50 等
        # filtered_scores = [s for s in score if s.get("xxx") == xxx]
        music_dict = {(str(item['id']), str(item['type']).lower()): item for item in MUSIC_DATA}
        
        scores_b35 = []
        scores_b15 = []

        for s in score:
            raw_id = s.get("id")
            if raw_id is None:
                continue
            # 处理id（可能会有bug，比如追加dx、sd谱面？
            if s.get("type") == "dx":
                song_id = f"{10000 + raw_id:05d}"
            else:
                song_id = f"1{raw_id}" if raw_id > 1000 else str(raw_id)

            song_info = music_dict.get((song_id, s.get("type")))
            if not song_info:
                continue
            # 判断是不是新歌（最新版本）
            is_new = song_info["basic_info"].get("is_new", False)
            if is_new:
                scores_b15.append(s)
            else:
                scores_b35.append(s)

        # 排序后取前 N 项
        scores_b35 = sorted(scores_b35, key=lambda x: x.get("dx_rating", 0), reverse=True)[:35]
        scores_b15 = sorted(scores_b15, key=lambda x: x.get("dx_rating", 0), reverse=True)[:15]
        rating_b35 = int(sum(song.get("dx_rating", 0) for song in scores_b35)) 
        rating_b15 = int(sum(song.get("dx_rating", 0) for song in scores_b15))
        rating = int(rating_b35 + rating_b15)


    # 补全b50（占位，不然分没打满会很丑
    scores_b35, scores_b15 = pad_b50(scores_b35, scores_b15)

    return templates.TemplateResponse("b50.html", {
        "request": request,
        "user_data": {
            "username": user_data.username, # 姓名，可以建个数据库自定义
            "nameplate": user_data.nameplate, # 姓名框，可以建个数据库自定义
            "icon": user_data.icon, # 头像，可以建个数据库自定义
            "rating_img": get_rating_img(rating)
            },
        "score_data": {
            "rating": rating,
            "rating_b35": rating_b35,
            "rating_b15": rating_b15,
            "scores_b35": scores_b35,
            "scores_b15": scores_b15
        },
        "get_difficulty_class": get_difficulty_class, # 模板样式类
        "get_fc_image": get_fc_image, 
        "get_fs_image": get_fs_image,
        "get_dxstars_image": get_dxstars_image
        })