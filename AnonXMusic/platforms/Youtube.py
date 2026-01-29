import os
import glob
import asyncio
import yt_dlp

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


class YouTubeAPI:

    async def url(self, message):
        if message.text:
            for word in message.text.split():
                if "youtu" in word:
                    return word
        return None

    async def download(self, link, mystic=None, video=False, **kwargs):
        loop = asyncio.get_running_loop()
        if video:
            return await loop.run_in_executor(None, self.video, link), False
        else:
            return await loop.run_in_executor(None, self.audio, link), False

    def audio(self, link):
        ydl_opts = {
            "format": "bestaudio",
            "outtmpl": f"{DOWNLOAD_DIR}/%(id)s.%(ext)s",
            "quiet": True,
            "no_warnings": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            vid = info["id"]

        return glob.glob(f"{DOWNLOAD_DIR}/{vid}.*")[0]

    def video(self, link):
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": f"{DOWNLOAD_DIR}/%(id)s.%(ext)s",
            "quiet": True,
            "no_warnings": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            vid = info["id"]

        return glob.glob(f"{DOWNLOAD_DIR}/{vid}.*")[0]