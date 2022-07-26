import ytdl.moviepy_pyinstaller_imports # PyInstaller requirement, do not remove
from pytube import YouTube, Playlist
from moviepy.editor import AudioFileClip
import toml
import sys
import os

class NoAudioMP4(Exception):
    def __init__(self, url):
        super().__init__("No audio stream in mp4 format found at {}".format(url))

class MP4FileNotFound(Exception):
    def __init__(self, path):
        super().__init__("No mp4 file found at {}".format(path))

def with_extension(filename: str, extension: str):
    return filename if filename.endswith("." + extension) else "{}.{}".format(filename, extension)

def move_mp4_to_mp3(filename, folder, erase_mp4 = True):
    mp4_file_path = os.path.join(folder, with_extension(filename, "mp4"))
    mp3_file_path = os.path.join(folder, with_extension(filename, "mp3"))

    if not(os.path.exists(mp4_file_path)):
        raise MP4FileNotFound(mp4_file_path)
    
    audio_file_clip=AudioFileClip(mp4_file_path)
    audio_file_clip.write_audiofile(mp3_file_path, verbose = False, logger = None)
    audio_file_clip.close()
    if erase_mp4:
        os.remove(mp4_file_path)

def get_audio_mp4_stream(youtube: YouTube):
    return youtube.streams.filter(only_audio=True, file_extension="mp4")

def download_audio_mp4(youtube: YouTube, filename, folder):
    audio = get_audio_mp4_stream(youtube)
    if len(audio) < 1:
        raise NoAudioMP4(youtube.js_url)

    audio[0].download(filename = with_extension(filename, "mp4"), output_path = folder)

def download_youtube_to_mp3(youtube_video_url, output_filename, folder = "."):
    yt = YouTube(url=youtube_video_url)
    download_audio_mp4(yt, output_filename, folder)
    move_mp4_to_mp3(output_filename, folder)

def usage_fn(all_args):
    def usage(_):
        print("Command >>>", "ytdl", *all_args, "<<< invalid")
        print("Usage :")
        print("\tytdl single <url> <filename>")
        print("\tytdl list <list_file_toml>")
        print("\tytdl format_playlist <url> <title>")
    return usage

def from_url(args):
    try:
        download_youtube_to_mp3(args[0], args[1])
    except Exception as e:
        print(e)

def from_config(args):
    toml_config = toml.load(args[0])
    for destination_folder, videos in toml_config.items():
        for title, params in videos.items():
            print(title, params["url"])
            try:
                download_youtube_to_mp3(params["url"], title, folder = destination_folder)
                print("\tOK")
            except Exception as e:
                print("\tFAIL", e)

def config_from_playlist_url(args):
    url = args[0]
    title = args[1]
    output_filename = args[2]
    playlist = Playlist(url)
    title_configs = {}
    for url in playlist.video_urls:
        video = YouTube(url)
        title_configs[video.title] = { "url": url }
    with open(with_extension(output_filename, "toml"), 'a') as output_file:
        toml.dump({title: title_configs}, output_file)

sub_commands = { "single": from_url, "list": from_config, "format_playlist": config_from_playlist_url }
def main(args):
    command = sub_commands.get(args[0], usage_fn(args))
    command(args[1:])

if __name__ == "__main__":
    main(sys.argv[1:])