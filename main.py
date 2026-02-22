from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp
import os
import re

app = FastAPI(title="AlloraPDF Instagram Downloader API")

# ==============================
# CORS Configuration
# ==============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://allorapdf.com",
        "https://www.allorapdf.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# Helper Function: URL Validation
# ==============================
def is_valid_instagram_url(url: str) -> bool:
    pattern = r"(https?://)?(www\.)?instagram\.com/"
    return re.match(pattern, url) is not None


# ==============================
# Health Check Route
# ==============================
@app.get("/")
async def root():
    return {"status": "API is running 🚀"}


# ==============================
# Download Endpoint
# ==============================
@app.get("/download")
async def download_video(url: str):
    try:
        if not is_valid_instagram_url(url):
            raise HTTPException(status_code=400, detail="Invalid Instagram URL")

        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "noplaylist": True,
            "cookiefile": "cookies.txt" if os.path.exists("cookies.txt") else None,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            if not info:
                raise HTTPException(status_code=404, detail="Unable to fetch media info")

            formats = info.get("formats", [])
            best_format = None

            for f in formats:
                if f.get("ext") == "mp4" and f.get("url"):
                    best_format = f
                    break

            if not best_format:
                raise HTTPException(status_code=404, detail="No downloadable video found")

            return {
                "title": info.get("title", "Instagram Video"),
                "thumbnail": info.get("thumbnail"),
                "download_url": best_format.get("url"),
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
