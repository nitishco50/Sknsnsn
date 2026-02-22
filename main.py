from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

# Allow frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://allorapdf.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/download")
async def download_video(url: str):
    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get("formats", [])
            
            for f in formats:
                if f.get("ext") == "mp4":
                    return {
                        "title": info.get("title"),
                        "download_url": f.get("url")
                    }

        raise HTTPException(status_code=404, detail="Video format not found")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
