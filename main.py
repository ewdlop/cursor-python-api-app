from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from gpt4all import GPT4All
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import TextClip
import os
import uuid
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = FastAPI(title="轻量级 AI 内容生成 API")

# 初始化模型
print("正在加载模型...")
text_model = GPT4All("ggml-gpt4all-j-v1.3-groovy")
print("模型加载完成！")

class TextRequest(BaseModel):
    prompt: str
    max_tokens: int = 100

class ImageRequest(BaseModel):
    text: str
    width: int = 512
    height: int = 512
    background_color: str = "white"
    text_color: str = "black"

class VideoRequest(BaseModel):
    text: str
    duration: int = 10

@app.post("/generate/text")
async def generate_text(request: TextRequest):
    try:
        response = text_model.generate(
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temp=0.7
        )
        return {"generated_text": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/image")
async def generate_image(request: ImageRequest):
    try:
        # 创建新图像
        image = Image.new('RGB', (request.width, request.height), request.background_color)
        draw = ImageDraw.Draw(image)
        
        # 尝试加载字体，如果失败则使用默认字体
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        # 在图像上绘制文本
        text_width = draw.textlength(request.text, font=font)
        text_height = 40
        position = ((request.width - text_width) // 2, (request.height - text_height) // 2)
        draw.text(position, request.text, fill=request.text_color, font=font)
        
        # 保存图像
        temp_file = f"temp_{uuid.uuid4()}.png"
        image.save(temp_file)
        return FileResponse(temp_file, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/video")
async def generate_video(request: VideoRequest):
    try:
        # 创建一个简单的文本视频
        temp_file = f"temp_{uuid.uuid4()}.mp4"
        text_clip = TextClip(request.text, fontsize=70, color='white', bg_color='black')
        text_clip = text_clip.set_duration(request.duration)
        text_clip.write_videofile(temp_file, fps=24)
        
        return FileResponse(temp_file, media_type="video/mp4")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 