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
with open("songs.json", "r", encoding="utf-8") as f:
    songs = json.load(f)

# with open("test1.json", "w", encoding="utf-8") as f:
#     json.dump(music_data, f)

if __name__ == "__main__":
   
    url = "http://127.0.0.1:13004/music_data?songid=820&type=sd&level_index=3"
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("请求成功")
    else:
        print("请求失败，状态码:", response.status_code)
        print("响应:", response.text)