from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from decimal import Decimal, ROUND_DOWN
from ..config import BASE_DIR
from ..utils import get_difficulty_class, get_fc_image, get_fs_image

router = APIRouter()
templates_mai_b50 = Jinja2Templates(directory=BASE_DIR / "src" / "web" / "templates")

def format_percent(value):
    # 保留 8 位小数，乘以 100 转为百分比，最后加上 %
    percent_value = Decimal(str(value)) * 100
    formatted = percent_value.quantize(Decimal('0.00000'), rounding=ROUND_DOWN)
    return f"{formatted}%"

def calculate_deductions(tap, hold, slide, touch, break_):
    total_score = (tap + touch) + hold * 2 + slide * 3 + break_ * 5
    deductions = {}
    deductions["TAP_GREAT"] = format_percent(0.2 / total_score)
    deductions["TAP_GOOD"] = format_percent(0.5 / total_score)
    deductions["TAP_MISS"] = format_percent(1.0 / total_score)

    deductions["HOLD_GREAT"] = format_percent(0.4 / total_score)
    deductions["HOLD_GOOD"] = format_percent(1.0 / total_score)
    deductions["HOLD_MISS"] = format_percent(2.0 / total_score)

    deductions["SLIDE_GREAT"] = format_percent(0.6 / total_score)
    deductions["SLIDE_GOOD"] = format_percent(1.5 / total_score)
    deductions["SLIDE_MISS"] = format_percent(3.0 / total_score)

    base_break = 5.0 / total_score
    bonus_break = 0.01 / break_
    deductions["BREAK_GREAT4x"] = format_percent(base_break * 0.2 + bonus_break * 0.6)
    deductions["BREAK_GREAT3x"] = format_percent(base_break * 0.4 + bonus_break * 0.6)
    deductions["BREAK_GREAT25x"] = format_percent(base_break * 0.5 + bonus_break * 0.6)
    deductions["BREAK_GOOD"] = format_percent(base_break * 0.6 + bonus_break * 0.7)
    deductions["BREAK_MISS"] = format_percent(base_break + bonus_break)
    deductions["BREAK_50"] = format_percent(bonus_break * 0.25)
    deductions["BREAK_100"] = format_percent(bonus_break * 0.5)
    return deductions

def calculate_tolerance_by_target(tap, hold, slide, touch, break_):
    total_score = tap * 500 + hold * 1000 + slide * 1500 + touch * 500 + break_ * 2500
    tolerance_dict = {}
    for target in [100.5, 100, 99.5, 99, 98, 97, 80]:
        lost_percent = 101 - target
        if lost_percent <= 0:
            tolerance = 0
        else:
            tolerance = (total_score * lost_percent / 10000)
        tolerance_dict[target] = round(tolerance, 2)
    return tolerance_dict


@router.get("/music_data", response_class=HTMLResponse)
async def music_data_view(request: Request):
    POST_DATA = request.app.state.POST_DATA
    if not POST_DATA:
        return HTMLResponse("<h1>无数据</h1>", status_code=404)

    minfo_data = POST_DATA.minfo_data
    type = minfo_data.type
    level_index = minfo_data.level_index
    minfo = minfo_data.minfo

    song = minfo["song"]
    scores = minfo["scores"]

    chart_type = "standard" if type == "sd" else "dx"
    chart_data = song["difficulties"].get(chart_type, [])

    score_map = {score["level_index"]: score for score in scores if score["type"] == chart_type}
    analysis_results = request.app.state.ANALYSIS_DATA

    special_breaks_map = {
        (int(item["song_id"]), item["difficulty_index"] - 1, item["chart_type"]): item["special_breaks"]
        for item in analysis_results
    }



    filled_scores = []
    for chart in chart_data:
        idx = chart["level_index"]
        tap = chart.get("tap_num", 0)
        hold = chart.get("hold_num", 0)
        slide = chart.get("slide_num", 0)
        touch = chart.get("touch_num", 0)
        break_num = chart.get("break_num", 0)

        total_notes = tap + hold + slide + touch + break_num

        score = score_map.get(idx, {
            "achievements": "未游玩",
            "fc": None,
            "fs": None,
            "dx_score": 0,
            "dx_rating": 0,
            "play_count": 0,
            "rate": None,
            "level": chart["level"],
            "level_index": idx,
            "type": chart_type,
            "id": song["id"],
            "title": song["title"],
            "level_value": chart["level_value"],
            "level_dx_score": 0
        })
        key = (int(song["id"]), idx, chart_type)
        score["special_breaks"] = special_breaks_map[key]

        # 计算扣分百分比
        deductions = calculate_deductions(tap, hold, slide, touch, break_num)
        tolerance = calculate_tolerance_by_target(tap, hold, slide, touch, break_num)

        score["deductions"] = deductions
        score["tolerance"] = tolerance

        # 附加数据
        score["total_notes"] = total_notes
        score["break_num"] = break_num

        filled_scores.append(score)

    minfo["scores"] = filled_scores

    return templates_mai_b50.TemplateResponse("music_data.html", {
        "request": request,
        "minfo": minfo,
        "chart_type": chart_type,
        "level_index": level_index,
        "get_difficulty_class": get_difficulty_class,
        "get_fc_image": get_fc_image,
        "get_fs_image": get_fs_image,
    })