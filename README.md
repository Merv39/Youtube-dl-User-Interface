# Youtube-dl-User-Interface

A work-in-progress interface for [youtube-dl](https://github.com/ytdl-org/youtube-dl) to reduce reliance on sketchy Youtube-to-mp3 and Youtube-to-mp4 sites.

<img width="1002" height="239" alt="image" src="https://github.com/user-attachments/assets/1a42d5fd-248d-488e-9898-a78e7e51d56a" />

Build Command:
'''
py -m PyInstaller --name yt_dl_gui --windowed --onefile `  --add-data "yt_dl_gui\options.json;yt_dl_gui"`
--add-binary "ffmpeg\ffmpeg.exe;ffmpeg" `  --add-binary "ffmpeg\ffprobe.exe;ffmpeg"`
yt_dl_gui\main.py
'''
