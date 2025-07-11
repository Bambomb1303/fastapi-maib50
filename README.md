# 舞萌成绩数据渲染

这是一个使用 **FastAPI + Jinja2 模板引擎** 构建的 Web 服务，用于将提交的舞萌成绩数据渲染为网页。

## 📁 项目结构

    .
    ├── main.py                # 主程序入口（服务端）
    ├── client.py              # 客户端示例
    ├── format_covers.py       # 曲绘文件名格式化工具
    ├── templates/
    │   └── b50.html           # b50页面模板（Jinja2）
    │   └── table.html         # 完成表、定数表页面模板（Jinja2）
    ├── static/
    │   └── img/               # 图片资源
    │   └── ...                # 字体、css 等资源
    ├── bests.json             # 最佳成绩
    ├── music_data.json        # 乐曲信息
    ├── players.json           # 用户信息
    ├── scores.json            # 成绩信息
    ├── README.md              # 项目说明
    └── requirements.txt       # 依赖列表

## 🚀 快速启动

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务

```bash
python main.py
```

默认运行在 `http://127.0.0.1:13004`

## ✅ 接口说明

### 1. POST `/`

用于提交用户信息与成绩数据，随后可在 GET `/b50` 页面查看渲染结果。

请求体结构（JSON）见 client.py


### 2. GET `/b50` `/table`

渲染最近提交的成绩页面，具体展示可由模板决定。

## 🧪 客户端示例

通过运行客户端程序 client.py，可自动读取本地的 json 文件，构造并发送 POST 请求：

```bash
python client.py
```

### music_data.json 数据来源于 [diving-fish](https://www.diving-fish.com/api/maimaidxprober/music_data)

### players.json bests.json scores.json 数据均来源于 [maimai_py](https://maimai.turou.fun/)


## 🎨 静态资源说明

### 应包含以下资源：

| 类型         | 文件路径示例                                |
| ------------ | ------------------------------------------- |
| 曲绘         | `/static/img/covers/*`                      |
| 用户头像     | `/static/img/icon/UI_Icon_000001.png`       |
| 称号框       | `/static/img/nameplate/UI_Plate_000000.png` |
| 其他 UI 图标 | `/static/img/ui/*`                          |

曲绘文件使用 [nonebot-plugin-maimaidx](https://github.com/Yuri-YuzuChaN/nonebot-plugin-maimaidx) 项目的静态资源素材

曲绘文件夹放入 `/static/img/` 后，运行 `format_covers.py` 可对文件名进行格式化

## ⚠️ 注意事项

1. 项目使用全局变量缓存最后一次 POST 数据，未持久化，仅演示用途；
2. 页面模板文件位于 `templates/` 目录下，可自行设计或修改；
3. 所有图片需放在 `/static/img/` 子目录中，路径需保持一致；
4. `user.icon` 和 `user.nameplate` 若自定义则应包含完整文件名，具体见 client.py ；
5. `music_data.json` 中须包含所有出现在成绩中的歌曲信息。

## 📄 项目参考

数据来源：[maimai_py](https://maimai.turou.fun/)

样式参考：[nonebot-plugin-maimaidx](https://github.com/Yuri-YuzuChaN/nonebot-plugin-maimaidx)

思路参考：[maimaiDX_yang](https://github.com/Dale2003/maimaiDX_yang)

## License

MIT License
