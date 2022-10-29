import os
from pathlib import Path
import youtube_dl
import sys


def extract_audio(code, audio_name='%(title)s'):
    # extract the audio from a video (with code <code>)

    _opts = {
        'outtmpl': f'{audio_name}.mp4',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(_opts) as ydl:
        ydl.download(['https://www.bilibili.com/video/%s' % code])
    return f'{audio_name}.mp3'


def cut_audio(input_path):
    """ use ffmpeg to cut audio first 10 seconds"""
    output_path = Path(input_path).parent.joinpath("out")
    output_path.mkdir(parents=True, exist_ok=True)
    output = str(output_path.absolute() / input_path)
    command = f"ffmpeg -ss 00:00:10 -i {input_path} {output}"
    print(command)
    os.system(command)


if __name__ == "__main__":
    arg_lens = len(sys.argv)
    if arg_lens < 2 or arg_lens > 4:
        raise RuntimeError("Invalid number of args. Please use right arguments.")

    method_name = sys.argv[1]
    if method_name == "-c" or method_name == "--cut":
        print("do cut job.")
        input_file = sys.argv[2]
        cut_audio(input_file)
    elif method_name == "-dc":
        print("download and cut first 10 seconds.")
        av_no = sys.argv[2]
        name = sys.argv[3]
        file_name = extract_audio(av_no, name)
        cut_audio(file_name)
    else:
        av_no = sys.argv[1]
        name = sys.argv[2]
        print("do download job.")
        file_name = extract_audio(av_no, name)
    print("Finished.")
