# import openai
# import requests
import time

# from pydub import AudioSegment
import os
from pytube import YouTube
from moviepy.editor import *

# import requests
# from api_key import api_openai_key, eleven_labs_api
# import generate_audio


# eleven_labs_api_key = eleven_labs_api
# openai.api_key = api_openai_key


def download_and_trim_audio(clip_url, filename, max_size):
    yt = YouTube(clip_url)
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(filename=f"{filename}.webm")

    audio = AudioFileClip(f"{filename}.webm")
    audio.write_audiofile(f"{filename}.mp3")

    file_size = os.path.getsize(f"{filename}.mp3") / (1024 * 1024)
    initial_duration = audio.duration

    if file_size > max_size:
        new_duration = (max_size / file_size) * initial_duration
        audio = audio.subclip(0, new_duration)
        audio.write_audiofile(f"{filename}.mp3")

        final_duration = audio.duration
        print(f"Initial duration: {initial_duration:.2f} seconds")
        print(f"Final duration: {final_duration:.2f} seconds")
        print(f"Trimmed: {initial_duration - final_duration:.2f} seconds")
