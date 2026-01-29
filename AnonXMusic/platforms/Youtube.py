import os
import re
import glob
import asyncio
import yt_dlp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython import VideosSearch
from AnonXMusic.utils.formatters import time_to_seconds


DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(youtube\.com|youtu\.be)"

    # -------- URL EXTRACT ----------
    async def url(self, message: Message):
        messages = [message]
        if message.reply_to_message:
            messages.append(message.reply_to_message)

        for msg in messages:
            if msg.entities:
                for entity in msg.entities:
                    if entity.type == MessageEntityType.URL:
                        text = msg.text or msg.caption
                        return text[
                            entity.offset : entity.offset + entity.length
                        ]
        return None

    # -------- VIDEO DETAILS ----------
    async def details(self, link):
        if "&" in link:
            link = link.split("&")[0]

        search = VideosSearch(link, limit=1)
        r = (await search.next())["result"][0]

        title = r["title"]
        duration_min = r["duration"]
        duration_sec = int(time_to_seconds(duration_min))
        thumb = r["thumbnails"][0]["url"].split("?")[0]
        vidid = r["id"]

        return title, duration_min, duration_sec, thumb, vidid

    async def title(self, link):
        return (await self.details(link))[0]

    async def duration(self, link):
        return (await self.details(link))[1]

    async def thumbnail(self, link):
        return (await self.details(link))[3]

    async def track(self, link):
        title, duration_min, _, thumb, vidid = await self.details(link)
        return {
            "title": title,
            "link": self.base + vidid,
            "vidid": vidid,
            "duration_min": duration_min,
            "thumb": thumb,
        }, vidid

    # -------- DOWNLOAD ----------
    async def download(self, link, mystic=None, video=False, **kwargs):
        loop = asyncio.get_running_loop()
        if video:
            return await loop.run_in_executor(None, self._video, link), False
        else:
            return await loop.run_in_executor(None, self._audio, link), False

    def _audio(self, link):
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{DOWNLOAD_DIR}/%(id)s.%(ext)s",
            "quiet": True,
            "no_warnings": True,
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
        return files[0]

    def _video(self, link):
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": f"{DOWNLOAD_DIR}/%(id)s.%(ext)s",
            "quiet": True,
            "no_warnings": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            vid = info["id"]

        files = glob.glob(f"{DOWNLOAD_DIR}/{vid}.*")
        return files[0]