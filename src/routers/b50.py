# routers/b50.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..config import BASE_DIR, MUSIC_DATA
from ..utils import get_rating_img, pad_b50, get_difficulty_class, get_fc_image, get_fs_image, get_dxstars_image, get_dxstars

router = APIRouter()
templates_mai_b50 = Jinja2Templates(directory=BASE_DIR / "src" / "web" / "templates")

@router.get("/b50", response_class=HTMLResponse)
async def _(request: Request):
    POST_DATA = request.app.state.POST_DATA
    if not POST_DATA:
        return HTMLResponse("<h1>无数据</h1>", status_code=404)

    user_data = POST_DATA.user_data

    if POST_DATA.scores_b50_data:
        rating = POST_DATA.scores_b50_data["rating"]
        rating_b35 = POST_DATA.scores_b50_data["rating_b35"]
        rating_b15 = POST_DATA.scores_b50_data["rating_b15"]
        scores_b35 = POST_DATA.scores_b50_data["scores_b35"]
        scores_b15 = POST_DATA.scores_b50_data["scores_b15"]
        for chart in scores_b35:
            chart["user_score"] = {
                "achievements": chart.get("achievements", 0),
                "dx_rating": chart.get("dx_rating", 0),
                "type": chart.get("type", "standard"),
                "level_value": chart.get("level_value", 0),
                "dx_score": chart.get("dx_score", 0),
                "level_dx_score": chart.get("level_dx_score", 0),
                "fc": chart.get("fc"),
                "fs": chart.get("fs")
            }
        for chart in scores_b15:
            chart["user_score"] = {
                "achievements": chart.get("achievements", 0),
                "dx_rating": chart.get("dx_rating", 0),
                "type": chart.get("type", "standard"),
                "level_value": chart.get("level_value", 0),
                "dx_score": chart.get("dx_score", 0),
                "level_dx_score": chart.get("level_dx_score", 0),
                "fc": chart.get("fc"),
                "fs": chart.get("fs")
            }
    else:
        scores_data = POST_DATA.scores_data
        config_data = POST_DATA.config_data

        if config_data.completion == "fs":
            filtered_scores = [s for s in scores_data if s.get("fs") == 1]
        elif config_data.completion == "fs+":
            filtered_scores = [s for s in scores_data if s.get("fs") == 2]
        elif config_data.completion == "fdx":
            filtered_scores = [s for s in scores_data if s.get("fs") == 3]
        elif config_data.completion == "fdx+":
            filtered_scores = [s for s in scores_data if s.get("fs") == 4]

        elif config_data.completion == "fc":
            filtered_scores = [s for s in scores_data if s.get("fc") == 3]
        elif config_data.completion == "fc+":
            filtered_scores = [s for s in scores_data if s.get("fc") == 2]
        elif config_data.completion == "ap":
            filtered_scores = [s for s in scores_data if s.get("fc") == 1]
        elif config_data.completion == "ap+":
            filtered_scores = [s for s in scores_data if s.get("fc") == 0]
        
        elif config_data.completion == "五星":
            filtered_scores = [s for s in scores_data if get_dxstars(s.get("dx_score", 0), s.get("level_dx_score", 0)) == "五星"]
        elif config_data.completion == "四星":
            filtered_scores = [s for s in scores_data if get_dxstars(s.get("dx_score", 0), s.get("level_dx_score", 0)) == "四星"]
        elif config_data.completion == "三星":
            filtered_scores = [s for s in scores_data if get_dxstars(s.get("dx_score", 0), s.get("level_dx_score", 0)) == "三星"]
        elif config_data.completion == "二星":
            filtered_scores = [s for s in scores_data if get_dxstars(s.get("dx_score", 0), s.get("level_dx_score", 0)) == "二星"]
        elif config_data.completion == "一星":
            filtered_scores = [s for s in scores_data if get_dxstars(s.get("dx_score", 0), s.get("level_dx_score", 0)) == "一星"]

        else:
            filtered_scores = scores_data




        def score_key(score):
            return (score["title"], score["type"], score["level_index"])

        score_map = {score_key(score): score for score in filtered_scores}

        scores_b35 = []
        scores_b15 = []

        for song in MUSIC_DATA:
            for chart_type in ("standard", "dx"):
                for chart in song["difficulties"].get(chart_type, []):
                    chart["title"] = song["title"]
                    chart["id"] = song["id"]
                    chart["type"] = chart_type
                    chart["level_dx_score"] = chart.get("level_dx_score", 0)
                    key = (chart["title"], chart["type"], chart["level_index"])
                    chart["user_score"] = score_map.get(key, None)

                    if chart["user_score"] and chart["user_score"].get("dx_rating") is not None:
                        version = chart.get("version", 0)
                        if version >= 25000 and version < 26000:
                            scores_b15.append(chart)
                        else:
                            scores_b35.append(chart)

        # 排序并裁剪
        scores_b35 = sorted(scores_b35, key=lambda x: x["user_score"]["dx_rating"], reverse=True)[:35]
        scores_b15 = sorted(scores_b15, key=lambda x: x["user_score"]["dx_rating"], reverse=True)[:15]

        rating_b35 = int(sum(c["user_score"]["dx_rating"] for c in scores_b35))
        rating_b15 = int(sum(c["user_score"]["dx_rating"] for c in scores_b15))
        rating = rating_b35 + rating_b15

    # 补全空位
    scores_b35, scores_b15 = pad_b50(scores_b35, scores_b15)

    return templates_mai_b50.TemplateResponse("b50.html", {
        "request": request,
        "user_data": {
            "username": user_data.username,
            "nameplate": user_data.nameplate,
            "icon": user_data.icon,
            "rating_img": get_rating_img(rating)
        },
        "score_data": {
            "rating": rating,
            "rating_b35": rating_b35,
            "rating_b15": rating_b15,
            "scores_b35": scores_b35,
            "scores_b15": scores_b15
        },
        "get_difficulty_class": get_difficulty_class,
        "get_fc_image": get_fc_image,
        "get_fs_image": get_fs_image,
        "get_dxstars_image": get_dxstars_image
    })
