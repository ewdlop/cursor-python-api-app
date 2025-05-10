from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from gpt4all import GPT4All
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
import os
import uuid
from dotenv import load_dotenv

import os
os.environ['IMAGEMAGICK_BINARY'] = '/opt/homebrew/bin/convert'

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
    width: int = 640
    height: int = 480
    fps: int = 30
    background_color: tuple = (0, 0, 0)  # 黑色背景
    text_color: tuple = (255, 255, 255)  # 白色文字

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
        # 创建视频写入器
        temp_file = f"temp_{uuid.uuid4()}.mp4"
        
        # 使用 H.264 编码器
        if os.name == 'nt':  # Windows
            fourcc = cv2.VideoWriter_fourcc(*'H264')
        else:  # macOS/Linux
            fourcc = cv2.VideoWriter_fourcc(*'avc1')
            
        out = cv2.VideoWriter(temp_file, fourcc, request.fps, (request.width, request.height))
        
        if not out.isOpened():
            raise Exception("无法创建视频文件")
        
        # 计算总帧数
        total_frames = request.duration * request.fps
        
        # 创建文本图像
        for _ in range(total_frames):
            # 创建黑色背景
            frame = np.full((request.height, request.width, 3), request.background_color, dtype=np.uint8)
            
            # 添加文本
            font = cv2.FONT_HERSHEY_SIMPLEX
            text_size = cv2.getTextSize(request.text, font, 1, 2)[0]
            text_x = (request.width - text_size[0]) // 2
            text_y = (request.height + text_size[1]) // 2
            
            cv2.putText(frame, request.text, (text_x, text_y), font, 1, request.text_color, 2)
            
            # 写入帧
            out.write(frame)
        
        # 释放视频写入器
        out.release()
        
        # 验证文件是否成功创建
        if not os.path.exists(temp_file) or os.path.getsize(temp_file) == 0:
            raise Exception("视频文件创建失败")
            
        return FileResponse(temp_file, media_type="video/mp4")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 