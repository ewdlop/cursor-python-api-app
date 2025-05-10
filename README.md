# 轻量级 AI 内容生成 API

这是一个使用 FastAPI 构建的轻量级 AI 内容生成 API，可以生成文本、图像和视频内容。所有功能都使用轻量级库，无需大型模型。

## 功能特点

- 文本生成：使用 GPT4All 生成文本
- 图像生成：使用 PIL 创建文本图像
- 视频生成：使用 MoviePy 创建简单的文本视频

## 系统要求

- Python 3.8+
- 至少 4GB RAM
- 至少 2GB 可用磁盘空间

## 安装

1. 克隆仓库：
```bash
git clone <repository-url>
cd <repository-name>
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 运行

启动服务器：
```bash
python main.py
```

服务器将在 http://localhost:8000 运行

## API 端点

### 生成文本
- 端点：`POST /generate/text`
- 请求体：
```json
{
    "prompt": "你的提示文本",
    "max_tokens": 100
}
```

### 生成图像
- 端点：`POST /generate/image`
- 请求体：
```json
{
    "text": "要显示的文本",
    "width": 512,
    "height": 512,
    "background_color": "white",
    "text_color": "black"
}
```

### 生成视频
- 端点：`POST /generate/video`
- 请求体：
```json
{
    "text": "要显示的文字",
    "duration": 10
}
```

## 注意事项

- 首次运行时，程序会自动下载 GPT4All 模型文件
- 生成的临时文件会自动保存在服务器上
- 建议在生产环境中实现文件清理机制
- 图像生成功能目前只支持文本到图像的转换 