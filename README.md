# 舞萌成绩数据渲染
    
  这是一个使用 **FastAPI + Jinja2 模板引擎** 构建的 Web 服务，用于将提交的舞萌成绩数据渲染为网页。


## 📁 项目结构
    
   
    
    .
    ├── main.py                # 主程序入口（服务端）
    ├── client.py              # 客户端示例
    ├── format_covers.py       # 曲绘文件名格式化工具
    ├── templates/
    │   └── b50.html           # 页面模板（Jinja2）
    ├── static/
    │   └── img/               # 图片资源
    │   └── ...                # 字体、css 等资源
    ├── scores_data.json       # 示例成绩数据
    ├── music_data.json        # 示例乐曲信息
    ├── README.md              # 项目说明
    └── requirements.txt       # 依赖列表
    


## 🚀 快速启动

  ### 1. 安装依赖
      
  ```bash
  pip install -r requirements.txt
  ````

  ### 2. 启动服务
    
  ```bash
  python main.py
  ```
    
默认运行在 `http://127.0.0.1:13003`


## ✅ 接口说明

  ### 1. POST `/b50`
  
  用于提交用户信息与成绩数据，随后可在 GET `/b50` 页面查看渲染结果。
  
  #### 请求体结构（JSON）：
  
  ```json
  {
    "user": {
      "username": "username",
      "nameplate": "UI_Plate_000000.png",
      "icon": "UI_Icon_000001.png"
    },
    "score": {
      "scores": [
        {
          "id": 719,
          "level_index": 3,
          "achievements": 101.0,
          "fc": 0,
          "fs": 4,
          "dx_score": 3315,
          "dx_rating": 321.0,
          "type": "standard",
          "title": "エンドマークに希望と涙を添えて",
          "level_value": 14.3,
          "level_dx_score": 3315
        }
      ]
    }
  }
  ```

  ### 2. GET `/b50`
    
  渲染最近提交的成绩页面，具体展示可由模板决定。


## 🧪 客户端示例
      
  通过运行客户端脚本 client.py，可自动读取本地的 music_data.json 与 scores_data.json，构造并发送 POST 请求：
  
  ```bash
  python client.py
  ```
  
  ### music_data.json 格式示例
  
  ```json
  [
    {
      "id": "719",
      "title": "エンドマークに希望と涙を添えて",
      "type": "SD",
      "basic_info": {
        "is_new": false
      }
    }
  ]
  ```
  
  ### scores_data.json 格式示例
  
  ```json
  [
    {
      "id": 719,
      "level_index": 3,
      "achievements": 101.0,
      "fc": 0,
      "fs": 4,
      "dx_score": 3315,
      "dx_rating": 321.0,
      "type": "standard",
      "title": "エンドマークに希望と涙を添えて",
      "level_value": 14.3,
      "level_dx_score": 3315
    }
  ]
  ```
  

## 🎨 静态资源说明
  
  ### 应包含以下资源：
  
  | 类型          | 文件路径示例                                                |
  | ----------- | ----------------------------------------------------- |
  | 曲绘        | `/static/img/covers/*`         |
  | 用户头像        | `/static/img/icon/UI_Icon_000001.png`         |
  | 称号框         | `/static/img/nameplate/UI_Plate_000000.png`   |
  | 其他 UI 图标        | `/static/img/ui/*`        |
  
  曲绘文件使用 [nonebot-plugin-maimaidx](https://github.com/Yuri-YuzuChaN/nonebot-plugin-maimaidx) 项目的静态资源素材
  
  曲绘文件夹放入 `/static/img/` 后，运行 `format_covers.py` 可对文件名进行格式化


## ⚠️ 注意事项

  1. 项目使用全局变量缓存最后一次 POST 数据，未持久化，仅演示用途；
  2. 页面模板文件位于 `templates/b50.html`，可自行设计或修改；
  3. 所有图片需放在 `/static/img/` 及子目录中，路径需保持一致；
  4. `user.icon` 和 `user.nameplate` 应包含完整文件名；
  5. 若 `scores_data.json` 中存在 ID 为 `1000-9999` ，请转为字符串并前缀 `1`，以便与 `music_data.json` 的 ID 对齐；
  
      例：1017 → "11017"
     
  6. `music_data.json` 中须包含所有出现在成绩中的歌曲信息。
  

## 📄 项目参考

  样式参考：[nonebot-plugin-maimaidx](https://github.com/Yuri-YuzuChaN/nonebot-plugin-maimaidx)
  思路参考：[maimaiDX_yang](https://github.com/Dale2003/maimaiDX_yang)


## License
  
  MIT License
