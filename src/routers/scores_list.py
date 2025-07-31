# routers/b50.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..config import BASE_DIR, MUSIC_DATA, VERSION_RANGE_MAP
from ..utils import get_rating_img, get_difficulty_class, get_fc_image, get_fs_image, get_dxstars_image

router = APIRouter()
templates_mai_b50 = Jinja2Templates(directory=BASE_DIR / "src" / "web" / "templates")
@router.get("/scores_list", response_class=HTMLResponse)
async def scores_list(request: Request):
    POST_DATA = request.app.state.POST_DATA
    if not POST_DATA:
        return HTMLResponse("<h1>无数据</h1>", status_code=404)

    user_data = POST_DATA.user_data
    scores_data = POST_DATA.scores_data
    config_data = POST_DATA.config_data

    # --- 筛选条件 ---
    target_level = config_data.level
    version_filter = config_data.version

    level_start = level_end = None
    if target_level:
        if target_level.endswith('+'):
            base_level = target_level[:-1]
            level_start = float(f"{base_level}.6")
            level_end = float(f"{base_level}.9")
        else:
            level_float = float(target_level)
            if '.' in target_level:
                level_start = level_end = level_float
            else:
                level_start = float(f"{target_level}.0")
                level_end = float(f"{target_level}.5")

    version_range = None
    start_ver = end_ver = None
    if version_filter:
        version_filter = version_filter
        version_range = VERSION_RANGE_MAP.get(version_filter)
        if version_range:
            start_ver, end_ver = version_range

    def score_key(score):
        return (score["title"], score["type"], score["level_index"])

    score_map = {score_key(score): score for score in scores_data}

    all_charts = []

    for song in MUSIC_DATA:
        for chart_type in ("standard", "dx"):
            for chart in song["difficulties"].get(chart_type, []):
                chart["title"] = song["title"]
                chart["id"] = song["id"]
                chart["type"] = chart_type
                chart["version"] = song.get("version", 0)
                chart["level_value"] = chart.get("level_value", 0)
                chart["level"] = chart.get("level", "?")
                chart["level_index"] = chart.get("level_index", 0)

                key = (chart["title"], chart["type"], chart["level_index"])
                chart["user_score"] = score_map.get(key)

                if not chart["user_score"]:
                    continue
                
                # --- 筛选定数 ---
                lv = float(chart.get("level_value") or 0)
                if level_start is not None and lv < level_start:
                    continue
                if level_end is not None and lv > level_end:
                    continue

                # --- 筛选版本 ---
                if start_ver is not None and end_ver is not None:
                    if not (start_ver <= chart["version"] < end_ver):
                        continue

                all_charts.append(chart)

    all_charts = sorted(all_charts, key=lambda x: x["user_score"]["achievements"], reverse=True)
    # 计算平均成绩
    if all_charts:
        total_achievements = sum(chart["user_score"]["achievements"] for chart in all_charts)
        average_achievements = total_achievements / len(all_charts)
    else:
        average_achievements = None


    return templates_mai_b50.TemplateResponse("scores_list.html", {
        "request": request,
        "user_data": {
            "username": user_data.username,
            "nameplate": user_data.nameplate,
            "icon": user_data.icon,
            "rating": user_data.rating,
            "rating_img": get_rating_img(user_data.rating)
        },
        "score_data": {
            "scores": all_charts
        },
        "average_achievements": average_achievements,
        "get_difficulty_class": get_difficulty_class,
        "get_fc_image": get_fc_image,
        "get_fs_image": get_fs_image,
        "get_dxstars_image": get_dxstars_image
    })