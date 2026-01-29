import os
import glob
import yt_dlp
import asyncio

DOWNLOAD_DIR = "downloads"

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)


ydl_opts_audio = {
    "format": "bestaudio/best",
    "outtmpl": f"{DOWNLOAD_DIR}/%(id)s.%(ext)s",
    "quiet": True,
    "nocheckcertificate": True,
    "ignoreerrors": True,
    "no_warnings": True,
    "geo_bypass": True,
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
}

ydl_opts_video = {
    "format": "bestvideo+bestaudio/best",
    "outtmpl": f"{DOWNLOAD_DIR}/%(id)s.%(ext)s",
    "quiet": True,
    "nocheckcertificate": True,
    "ignoreerrors": True,
    "no_warnings": True,
    "geo_bypass": True,
}


async def _run_ydl(opts, url):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: _ydl_download(opts, url))


def _ydl_download(opts, url):
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return info.get("id")


async def download_audio(url):
    video_id = await _run_ydl(ydl_opts_audio, url)
    files = glob.glob(f"{DOWNLOAD_DIR}/{video_id}.*")
    if not files:
        raise FileNotFoundError("Audio file not found")
    return files[0]


async def download_video(url):
    video_id = await _run_ydl(ydl_opts_video, url)
    files = glob.glob(f"{DOWNLOAD_DIR}/{video_id}.*")
    if not files:
        raise FileNotFoundError("Video file not found")
    return files[0]


# MAIN FUNCTION (play command uses this)
async def get_youtube(url, video=False):
    """
    Returns:
    file_path, direct(False)
    """

    if video:
        file = await download_video(url)
    else:
        file = await download_audio(url)

    return file, False