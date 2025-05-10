# AI 内容生成 API

这是一个使用 FastAPI 构建的 AI 内容生成 API，可以生成文本、图像和视频内容。

## 功能特点

- 文本生成：使用 OpenAI 的 GPT 模型生成文本
- 图像生成：使用 Stability AI 的模型生成图像
- 视频生成：使用 MoviePy 创建简单的文本视频

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

3. 创建 `.env` 文件并添加必要的 API 密钥：
```
OPENAI_API_KEY=your_openai_api_key
STABILITY_API_KEY=your_stability_api_key
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
    "prompt": "图像描述",
    "width": 512,
    "height": 512
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

- 确保您有有效的 API 密钥
- 生成的临时文件会自动保存在服务器上
- 建议在生产环境中实现文件清理机制 