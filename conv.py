import os
import yt_dlp

# Function to download a mp3 or mp4-file
def download_mp3(url, path, mp4=False):
    os.makedirs(path, exist_ok=True)
    if mp4==True:
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'noplaylist': False,
            'verbose': True,
        }
    else:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{path}/%(title)s.%(ext)s',  # Dateiname: Titel.mp3
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }
            ],
            'noplaylist': False
        }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])