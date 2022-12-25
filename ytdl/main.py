# PyInstaller requirement, do not remove
import ytdl.moviepy_pyinstaller_imports #type: ignore
from pytube import YouTube, Playlist, StreamQuery #type: ignore
from moviepy.editor import AudioFileClip #type: ignore
import toml
import sys
import os
import typer

class NoAudioMP4(Exception):
    def __init__(self, url: str):
        super().__init__("No audio stream in mp4 format found at {}".format(url))

class MP4FileNotFound(Exception):
    def __init__(self, path: str):
        super().__init__("No mp4 file found at {}".format(path))

def with_extension(filename: str, extension: str):
    return filename if filename.endswith("." + extension) else "{}.{}".format(filename, extension)

def move_mp4_to_mp3(filename: str, folder: str, erase_mp4: bool = True) -> None:
    mp4_file_path = os.path.join(folder, with_extension(filename, "mp4"))
    mp3_file_path = os.path.join(folder, with_extension(filename, "mp3"))

    if not(os.path.exists(mp4_file_path)):
        raise MP4FileNotFound(mp4_file_path)
    
    audio_file_clip=AudioFileClip(mp4_file_path)
    audio_file_clip.write_audiofile(mp3_file_path, verbose = False, logger = None)
    audio_file_clip.close()
    if erase_mp4:
        os.remove(mp4_file_path)

def get_audio_mp4_stream(youtube: YouTube) -> StreamQuery:
    return youtube.streams.filter(only_audio=True, file_extension="mp4") #type: ignore

def download_audio_mp4(youtube: YouTube, filename: str, folder: str) -> None:
    audio = get_audio_mp4_stream(youtube)
    if len(audio) < 1:
        raise NoAudioMP4(youtube.js_url)
    audio[0].download(filename = with_extension(filename, "mp4"), output_path = folder) #type: ignore

def download_youtube_to_mp3(youtube_video_url: str, output_filename: str, folder: str = "."):
    yt = YouTube(url=youtube_video_url)
    download_audio_mp4(yt, output_filename, folder)
    move_mp4_to_mp3(output_filename, folder)

app = typer.Typer()

@app.command(name="single")
def from_url(video_url: str, output_filename: str):
    try:
        download_youtube_to_mp3(video_url, output_filename)
    except Exception as e:
        print(e)

@app.command(name="list")
def from_config(config_file: str):
    toml_config = toml.load(config_file)
    for destination_folder, videos in toml_config.items():
        for title, params in videos.items():
            print(title, params["url"])
            try:
                download_youtube_to_mp3(params["url"], title, folder = destination_folder)
                print("\tOK")
            except Exception as e:
                print("\tFAIL", e)

@app.command(name="format_playlist")
def config_from_playlist_url(url: str, title: str, output_config_file: str):
    playlist = Playlist(url)
    title_configs: dict[str, dict[str, str]] = {}
    for url in playlist.video_urls:
        video = YouTube(url)
        title_configs[video.title] = { "url": url }
    with open(with_extension(output_config_file, "toml"), 'a') as output_file:
        toml.dump({title: title_configs}, output_file)

def main(args: list[str]):
    app(args)

if __name__ == "__main__":
    main(sys.argv[1:])