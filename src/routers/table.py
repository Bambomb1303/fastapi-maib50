# routers/comp.py
from collections import Counter
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..config import BASE_DIR, MUSIC_DATA, version_map
from ..utils import group_scores, get_difficulty_class, calculate_counters

router = APIRouter()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@router.get("/table", response_class=HTMLResponse)
async def _(request: Request):
    POST_DATA = request.app.state.POST_DATA
    if not POST_DATA:
        return HTMLResponse("<h1>无数据</h1>", status_code=404)
    
    # 解构数据：分数数据和配置数据
    scores_data = POST_DATA.scores_data  # 玩家分数
    config_data = POST_DATA.config_data  # 筛选配置

    # --- 处理等级筛选条件 ---
    level = config_data.level
    level_start = level_end = None
    if level:
        # 处理+号等级（如13+）
        if level.endswith('+'):
            level_start = f"{level[:-1]}.6"  # （如13.6）
            level_end = f"{level[:-1]}.9"    # （如13.9）
        else:
            level_start = f"{level}.0"  # （如13.0）
            level_end = f"{level}.5"    # （如13.5）

    # --- 处理版本筛选条件 ---
    version = config_data.version
    if version:
        # 版本映射表（如"2025"->"prism"）
        version = version_map.get(version, version)

    # --- 处理完成度类型 ---
    # 统一完成度标识到三种类型：fc(全连)/fs(全良)/rate(完成率)
    completion = config_data.completion.lower()
    if completion in ["ap", "ap+", "fc", "fc+"]:  # AP/FC相关类型
        config_data.completion = "fc"
    elif completion in ["fs", "fs+", "fdx", "fdx+"]:  # FS相关类型
        config_data.completion = "fs"
    else:  # 默认显示完成率
        config_data.completion = "rate"

    # --- 筛选符合条件的谱面数据 ---
    music_data = []
    for song in MUSIC_DATA:
        ds_list = song.get("ds", [])  # 各难度定数列表
        from_str = song.get("basic_info", {}).get("from", "")  # 所属版本
        raw_id = (song.get("id"))

        # 跳过宴谱
        if len(raw_id) == 6:
            continue
            
        # 处理歌曲ID格式
        if song.get("type").lower() == "dx":
            song_id = raw_id[1:]   # 去掉前缀 1
            song_id = song_id.lstrip("0")  # 去除前导零
        else:  # 标准谱面
            song_id = str(raw_id)

        # 遍历每个难度级别
        for idx, ds_value in enumerate(ds_list):
            ds_float = float(ds_value)
            
            # 等级筛选
            if level_start is not None and not (float(level_start) <= ds_float <= float(level_end)):
                continue

            # 版本筛选
            if version and version not in from_str:
                continue

            music_data.append({
                "id": song_id,
                "title": song.get("title"),
                "type": song.get("type"),
                "level_index": idx,
                "level": ds_float,
                "from": song.get("basic_info", {}).get("from")  # 所属版本
            })
    
    # 判断是否使用具体定数（例如13是否要拆成13.0-13.5）
    music_data = group_scores(music_data, version and "table_type" != "b50")

    # --- 处理玩家分数数据 ---
    # 创建以(id, 难度索引, 类型)为键的分数字典
    scores_data = {
        (str(item['id']), int(item['level_index']), str(item['type']).lower()): item
        for item in scores_data
        if 'id' in item and 'level_index' in item and 'type' in item
    }
    
    # 计算各类计数器（FC/FS/RATE）
    fc_counter, fs_counter, rate_counter = calculate_counters(
        scores_data, 
        music_data, 
        config_data
    )

    return templates.TemplateResponse("table.html", {
        "request": request,
        "music_data": music_data,
        "scores_data": scores_data,
        "config_data": config_data,
        "get_difficulty_class": get_difficulty_class,  # 模板使用的难度类（样式需要）
        "fc_counter": fc_counter,  # FC计数器数据
        "fs_counter": fs_counter,  # FS计数器数据
        "rate_counter": rate_counter,  # rate计数器数据
    })