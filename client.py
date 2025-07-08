import json
import requests
import sys
import os

# 添加当前目录到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 加载数据文件
with open("scores_data.json", "r", encoding="utf-8") as f:
    scores = json.load(f)
    
with open("music_data.json", "r", encoding="utf-8") as f:
    music_data = json.load(f)

# (可选) 筛选出 AP / AP+ 的成绩
# scores = [s for s in scores if s.get("fc") in [0, 1]]

# 创建歌曲ID到歌曲信息的映射字典
music_dict = {str(song["id"]): song for song in music_data}

# 初始化标准版和DX版最佳列表
sdBest = []
dxBest = []

# 处理每首歌曲分数
for score in scores:
    raw_id = score.get("id")
    if raw_id is None:
        continue
        
    # 处理歌曲ID格式（旧曲补1前缀）
    song_id = f"1{raw_id}" if raw_id > 1000 else str(raw_id)
    
    # 获取歌曲信息
    song_info = music_dict.get(song_id)
    if not song_info:
        continue
        
    # 根据是否是新版分类
    if song_info["basic_info"].get("is_new", False):
        dxBest.append(score)
    else:
        sdBest.append(score)

# 按DX Rating排序并截取最佳成绩
sdBest = sorted(sdBest, 
                key=lambda x: x.get("dx_rating", 0), 
                reverse=True)[:35]
                
dxBest = sorted(dxBest, 
                key=lambda x: x.get("dx_rating", 0), 
                reverse=True)[:15]

# 计算评级分数
rating_b35 = sum(song.get("dx_rating", 0) for song in sdBest)
rating_b15 = sum(song.get("dx_rating", 0) for song in dxBest)
rating = int(rating_b35 + rating_b15)

# 构建请求负载
payload = {
    "user": {
        "username": "str",
        "nameplate": "UI_Plate_000000.png",
        "icon": "UI_Icon_000001.png"
    },
    "score": {
        "scores": {
            "rating": int(rating),
            "rating_b35": int(rating_b35),
            "rating_b15": int(rating_b15),
            "scores_b35": sdBest,
            "scores_b15": dxBest
        }
    }
}

# 发送POST请求
url = "http://127.0.0.1:13003/b50"
headers = {"Content-Type": "application/json"}
response = requests.post(url, json=payload, headers=headers)
# 检查响应状态
if response.status_code == 200:
    print("请求成功")
else:
    print("请求失败，状态码:", response.status_code)