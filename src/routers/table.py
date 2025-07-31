# routers/comp.py
from collections import defaultdict
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..config import MUSIC_DATA, BASE_DIR
from ..utils import get_difficulty_class, calculate_counters


router = APIRouter()
templates_mai_b50 = Jinja2Templates(directory=BASE_DIR / "src" / "web" / "templates")

@router.get("/table", response_class=HTMLResponse)
async def _(request: Request):
    POST_DATA = request.app.state.POST_DATA
    if not POST_DATA:
        return HTMLResponse("<h1>无数据</h1>", status_code=404)
    
    # 解构数据：分数数据和配置数据
    scores_data = POST_DATA.scores_data  # 玩家分数
    config_data = POST_DATA.config_data  # 筛选配置
    if config_data.table_type == "定数表":
        scores_data = {}

    # --- 处理等级筛选条件 ---
    target_level = config_data.level
    level_start = level_end = None
    if target_level:
        if target_level.endswith('+'):
            base_level = target_level[:-1]
            level_start = f"{base_level}.6"
            level_end = f"{base_level}.9"
        else:
            level_float = float(target_level)
            # 如果是带小数（包含 .0）
            if '.' in target_level:
                level_start = level_end = str(level_float)
            else:
                level_start = f"{target_level}.0"
                level_end = f"{target_level}.5"

    # --- 处理完成度类型 ---
    completion = config_data.completion.lower()
    if completion in ["ap", "ap+", "fc", "fc+"]:  # AP/FC相关类型
        completion_type = "fc"
        
    elif completion in ["fs", "fs+", "fdx", "fdx+"]:  # FS相关类型
        completion_type = "fs"
    else:  # 默认显示完成率
        completion_type = "rate"
    config_data.completion_type = completion_type

    # 成绩索引 key 生成函数
    def score_key(score):
        return (score["title"], score["type"], score["level_index"])

    # 将成绩表做成映射以便快速查找
    score_map = {score_key(score): score for score in scores_data}

    # 搜索 + 合并 user_score 信息
    matched_charts_by_level = defaultdict(list)

    for song in MUSIC_DATA:
        for chart_type in ("standard", "dx"):
            for chart in song["difficulties"].get(chart_type, []):
                if float(level_start) <= float(chart["level_value"]) <= float(level_end):
                    # 添加基础信息（如 title、id）
                    chart["title"] = song["title"]
                    chart["id"] = song["id"]
                    chart["type"] = chart_type

                    # 查找成绩信息并附加
                    key = (chart["title"], chart["type"], chart["level_index"])
                    chart["user_score"] = score_map.get(key, None)

                    # 分组
                    matched_charts_by_level[chart["level_value"]].append(chart)

    for _, charts in matched_charts_by_level.items():
        # 根据 completion_type 设置排序参数
        if completion_type == "fs":
            default_value = -1
            reverse_sort = True
        else:
            default_value = 999
            reverse_sort = False

        charts.sort(
            key=lambda chart: (
                chart["user_score"][completion_type]
                if chart.get("user_score") and chart["user_score"].get(completion_type) is not None
                else default_value
            ),
            reverse=reverse_sort
        )

    # 排序后构建模板需要的数据格式
    music_data = sorted(matched_charts_by_level.items(), key=lambda x: x[0], reverse=True)

    fc_counter, fs_counter, rate_counter = calculate_counters(
        completion_type,
        music_data,
    )

    return templates_mai_b50.TemplateResponse("table.html", {
        "request": request,
        "music_data": music_data,
        "config_data": config_data,
        "get_difficulty_class": get_difficulty_class,  # 模板使用的难度类（样式需要）
        "fc_counter": fc_counter,  # FC计数器数据
        "fs_counter": fs_counter,  # FS计数器数据
        "rate_counter": rate_counter,  # rate计数器数据
    })