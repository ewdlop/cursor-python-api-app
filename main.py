from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import openai
import os
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from dotenv import load_dotenv
import tempfile
import uuid

# 加载环境变量
load_dotenv()

app = FastAPI(title="AI 内容生成 API")

# 配置 API 密钥
openai.api_key = os.getenv("OPENAI_API_KEY")
stability_api = client.StabilityInference(
    key=os.getenv("STABILITY_API_KEY"),
    verbose=True,
)

class TextRequest(BaseModel):
    prompt: str
    max_tokens: int = 100

class ImageRequest(BaseModel):
    prompt: str
    width: int = 512
    height: int = 512

class VideoRequest(BaseModel):
    text: str
    duration: int = 10

@app.post("/generate/text")
async def generate_text(request: TextRequest):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=request.prompt,
            max_tokens=request.max_tokens
        )
        return {"generated_text": response.choices[0].text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/image")
async def generate_image(request: ImageRequest):
    try:
        answers = stability_api.generate(
            prompt=request.prompt,
            seed=123,
            steps=30,
            cfg_scale=7.0,
            width=request.width,
            height=request.height,
            samples=1,
        )
        
        # 保存生成的图片
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.type == generation.ARTIFACT_IMAGE:
                    temp_file = f"temp_{uuid.uuid4()}.png"
                    with open(temp_file, "wb") as f:
                        f.write(artifact.binary)
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