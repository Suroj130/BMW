import os
import glob
import yt_dlp
import asyncio

DOWNLOAD_DIR = "downloads"

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)


class YouTubeAPI:
    def __init__(self):
        pass

    async def download(self, link, mystic=None, video=False, **kwargs):
        loop = asyncio.get_event_loop()

        if video:
            return await loop.run_in_executor(None, self._video, link), False
        else:
            return await loop.run_in_executor(None, self._audio, link), False

    def _audio(self, link):
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{DOWNLOAD_DIR}/%(id)s.%(ext)s",
            "quiet": True,
            "nocheckcertificate": True,
            "ignoreerrors": True,
            "no_warnings": True,
            "geo_bypass": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            vid = info["id"]

        files = glob.glob(f"{DOWNLOAD_DIR}/{vid}.*")
        if not files:
            raise FileNotFoundError("Audio file not found")

        return files[0]

    def _video(self, link):
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": f"{DOWNLOAD_DIR}/%(id)s.%(ext)s",
            "quiet": True,
            "nocheckcertificate": True,
            "ignoreerrors": True,
            "no_warnings": True,
            "geo_bypass": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            vid = info["id"]

        files = glob.glob(f"{DOWNLOAD_DIR}/{vid}.*")
        if not files:
            raise FileNotFoundError("Video file not found")

        return files[0]