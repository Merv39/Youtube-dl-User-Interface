from yt_dlp import YoutubeDL
import os
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(os.path.dirname(__file__))  # Change working directory to the script's directory

download_dir = os.path.join(project_dir, 'downloads')
os.makedirs(download_dir, exist_ok=True)

#check if ffmpeg exists, if not, download it
import shutil
ffmpeg_dir = shutil.which('ffmpeg')
if ffmpeg_dir:
    print(f'FFmpeg found at {ffmpeg_dir}.')
    ffmpeg_dir = os.path.dirname(ffmpeg_dir)
else:
    print('FFmpeg not found.')
    ffmpeg_dir = os.path.join(project_dir, 'ffmpeg')

def download_ffmpeg() -> None:
    import requests
    import zipfile
    import io
    import time
    import sys

    # URL of FFmpeg Essentials Build (Windows 64-bit)
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = os.path.join(ffmpeg_dir, 'ffmpeg.zip')

    print('Downloading FFmpeg...')
    response = requests.get(url=url, stream=True)
    downloaded = 0
    start_time = time.time()

    with open(zip_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            downloaded += len(chunk)
            elapsed_time = time.time() - start_time
            speed = downloaded / (1024*1024) / elapsed_time #MB/s
            sys.stdout.flush()
            sys.stdout.write('\rDownloading at {0:.2f} MB/s'.format(speed).ljust(30))

    #extract only ffmpeg.exe and ffprobe.exe
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.endswith('ffmpeg.exe') or file.endswith('ffprobe.exe'):
                # Extract to ffmpeg_dir, flattening the directory structure
                target_path = os.path.join(ffmpeg_dir, os.path.basename(file))
                with zip_ref.open(file) as source, open(target_path, 'wb') as target:
                    target.write(source.read())
    
    os.remove(zip_path)

if not (os.path.exists(os.path.join(ffmpeg_dir, 'ffmpeg.exe')) or os.path.exists(os.path.join(ffmpeg_dir, 'ffprobe.exe'))):
    download_ffmpeg()

def download_video(URL, format_type):
    # Open options from JSON file
    import json
    options_path = os.path.join(os.path.dirname(__file__), "options.json")
    with open(options_path, "r") as f:
        all_options = json.load(f) 
    
    # Select the specific format configuration
    ydl_options = all_options.get(format_type, all_options["mp3"])  # Default to mp3 if format not found

    # Add ffmpeg_location at runtime
    ydl_options["ffmpeg_location"] = ffmpeg_dir

    with YoutubeDL(ydl_options) as ydl:
        ydl.download([URL])