![CI-master](https://github.com/NyuB/youtube-mp3-downloader/actions/workflows/ci.yml/badge.svg?branch=master)

## Install/Bundle
### PyInstaller
#### Windows
```
.venv\activate
pip install -r requirements.txt
install
```
#### Linux
```
chmod +x install.sh
.venv/activate
pip install -r requirements.txt
./install.sh
```

## Usage
### Direct url download
```
.venv/Scripts/python -m ytdl.main single <youtube_video_url> <output_filename>
```
```
dist/ytdl single <youtube_video_url> <output_filename>
```
### From toml file
```
.venv/Scripts/python -m ytdl.main list <video_listing.toml>
```
```
dist/ytdl list <video_listing.toml>
```

#### Toml list file format
```
["<Destination Folder Name>"."<Music File Name>"]
url = "https://youtube.com/<source-video-ur>l"

["..".".."]
url = "...."

...
```