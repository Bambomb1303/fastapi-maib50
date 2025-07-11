import json
import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 加载数据文件（数据来源 maimai_py
with open("players.json", "r", encoding="utf-8") as f:
    players = json.load(f)
with open("scores.json", "r", encoding="utf-8") as f:
    scores = json.load(f)
with open("bests.json", "r", encoding="utf-8") as f:
    bests = json.load(f)
with open("music_data.json", "r", encoding="utf-8") as f:
    music_data = json.load(f)

if __name__ == "__main__":
    # 构建payload（具体见 models。若填写 scores_b50_data 则默认 b50
    payload = {
        "user_data": {
            "username": players["name"],
            "nameplate": "UI_Plate_300501.png",
            "icon": f"UI_Icon_{players["icon"]["id"]}.png"
        },
        "scores_b50_data": bests,
        "scores_data": scores,
        "config_data": {
                "table_type": "",
                "level": "",
                "version": "",
                "completion": ""
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