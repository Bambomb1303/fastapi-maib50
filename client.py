import json
import requests
import sys
import os
from pathlib import Path

data_dir = Path(__file__).parent / "client_data"

# 加载数据文件（数据来源 maimai_py
with open(data_dir / "players.json", "r", encoding="utf-8") as f:
    players = json.load(f)
with open(data_dir / "scores.json", "r", encoding="utf-8") as f:
    scores = json.load(f)
with open(data_dir / "bests.json", "r", encoding="utf-8") as f:
    bests = json.load(f)
with open(data_dir / "music_data.json", "r", encoding="utf-8") as f:
    music_data = json.load(f)
with open(data_dir / "songs.json", "r", encoding="utf-8") as f:
    songs = json.load(f)
with open(data_dir / "minfo.json", "r", encoding="utf-8") as f:
    minfo = json.load(f)

# with open("test1.json", "w", encoding="utf-8") as f:
#     json.dump(music_data, f)

if __name__ == "__main__":
    # 构建payload（具体见 models。若填写 scores_b50_data 则默认 b50
    payload = {
        "user_data": {
            "username": players["name"],
            "nameplate": "UI_Plate_300501.png",
            "icon": f"UI_Icon_{players['icon']['id']}.png",
            "rating": players["rating"],
        },
        "scores_data": scores,
        "config_data": {
                "table_type": "b50",
                "level": "",
                "version": "",
                "completion": "三星"
            }
        }
    
    payload = {
        "minfo_data": {
            "type": "dx",
            "level_index": 3,
            "minfo": minfo
        }
    }
    url = "http://127.0.0.1:13004/"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("请求成功")
    else:
        print("请求失败，状态码:", response.status_code)
        print("响应:", response.text)