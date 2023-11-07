from flask import Flask, render_template, request, redirect, url_for, send_file, abort
import openai
import shutil

# import requests
# import time
# from pydub import AudioSegment
import os

# from pytube import YouTube
from moviepy.editor import *
import requests

from api_key import api_openai_key, eleven_labs_api
import generate_audio
import url_video
import elevenlabs_api

directory_path = "Url_Audio"
directory_path1 = "Podcast_textfile"
directory_path2 = "Final_Audio"
directory_path3 = "Voice_Id_File"

# Create a Flask app
app = Flask(__name__)


eleven_labs_api_key = eleven_labs_api
openai.api_key = api_openai_key


@app.route("/download_audio")
def download_audio():
    audio_file = "Final_Audio/podcast.mp3"  # Path to your MP3 file
    return serve_file(audio_file, "podcast.mp3")


@app.route("/download_text")
def download_text():
    text_file = "Podcast_textfile/Podcast_Transcript.txt"  # Path to your .txt file
    return serve_file(text_file, "Podcast_Transcript.txt")


@app.route("/download_voice_id")
def download_voice_id():
    voice_id = "Voice_id_File/generated_voice_id.txt"  # Path to your .txt file
    return serve_file(voice_id, "generated_voice_id.txt")


def serve_file(file_path, download_name):
    try:
        return send_file(file_path, as_attachment=True, download_name=download_name)
    except FileNotFoundError:
        abort(404)


@app.errorhandler(404)
def file_not_found(error):
    return "File Not Found", 404


def delete_files_from_dic(directory):
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)


def save_voice_id(id_1, id_2):
    try:
        with open("Voice_id_File/generated_voice_id.txt", "w") as voiceid:
            voiceid.write(
                f"speaker one voice id: {id_1} \n speaker two voice id: {id_2}"
            )
    except:
        pass


# Define a route to display the form
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Process the form data here
        speaker_one_text = request.form["speaker_one_text"]

        speaker_two_text = request.form["speaker_two_text"]

        topic = request.form["topic"]

        num_turns = int(request.form["num_turns"])

        # Check how Speaker One information is provided (ID or URL)
        if (
            "speaker_one_option" in request.form
            and request.form["speaker_one_option"] == "id"
        ):
            speaker_one_id = request.form["speaker_one_id"]
            speaker_one_url = None  # Set to None since URL was not provided
        else:
            speaker_one_id = None  # Set to None since ID was not provided
            speaker_one_url = request.form["speaker_one_url"]

        # Check how Speaker Two information is provided (ID or URL)
        if (
            "speaker_two_option" in request.form
            and request.form["speaker_two_option"] == "id"
        ):
            speaker_two_id = request.form["speaker_two_id"]
            speaker_two_url = None  # Set to None since URL was not provided
        else:
            speaker_two_id = None  # Set to None since ID was not provided
            speaker_two_url = request.form["speaker_two_url"]

        speaker_one_voice_description = request.form["speaker_one_voice_description"]
        speaker_two_voice_description = request.form["speaker_two_voice_description"]

        delete_files_from_dic(directory_path)
        delete_files_from_dic(directory_path1)
        delete_files_from_dic(directory_path2)
        delete_files_from_dic(directory_path3)

        if speaker_one_url is not None and speaker_two_url is not None:
            url_video.download_and_trim_audio(
                speaker_one_url, f"{directory_path}/speaker_one", 9
            )

            voice_one_id = elevenlabs_api.upload_to_api(
                f"{directory_path}/speaker_one",
                "Podcast Voice #1",
                speaker_one_voice_description,
                eleven_labs_api_key,
            )

            url_video.download_and_trim_audio(
                speaker_two_url, f"{directory_path}/speaker_two", 9
            )

            voice_two_id = elevenlabs_api.upload_to_api(
                f"{directory_path}/speaker_two",
                "Podcast Voice #2",
                speaker_two_voice_description,
                eleven_labs_api_key,
            )

            save_voice_id(voice_one_id, voice_two_id)

            generate_audio.generate_podcast(
                speaker_one_text,
                speaker_two_text,
                voice_one_id,
                voice_two_id,
                topic,
                num_turns,
            )

        # if speaker_one_id is not None and speaker_two_id is not None:
        if speaker_one_id is not None and speaker_two_id is not None:
            print("idd")
            save_voice_id(speaker_one_id, speaker_two_id)

            generate_audio.generate_podcast(
                speaker_one_text,
                speaker_two_text,
                speaker_one_id,
                speaker_two_id,
                topic,
                num_turns,
            )

        if speaker_one_url is not None and speaker_two_id is not None:
            url_video.download_and_trim_audio(
                speaker_one_url, f"{directory_path}/speaker_one", 9
            )

            voice_one_id = elevenlabs_api.upload_to_api(
                f"{directory_path}/speaker_one",
                "Podcast Voice #1",
                speaker_one_voice_description,
                eleven_labs_api_key,
            )

            save_voice_id(voice_one_id, speaker_two_id)

            generate_audio.generate_podcast(
                speaker_one_text,
                speaker_two_text,
                voice_one_id,
                speaker_two_id,
                topic,
                num_turns,
            )

        if speaker_one_id is not None and speaker_two_url is not None:
            url_video.download_and_trim_audio(
                speaker_two_url, f"{directory_path}/speaker_two", 9
            )

            voice_two_id = elevenlabs_api.upload_to_api(
                f"{directory_path}/speaker_two",
                "Podcast Voice #2",
                speaker_two_voice_description,
                eleven_labs_api_key,
            )

            save_voice_id(speaker_one_id, voice_two_id)

            generate_audio.generate_podcast(
                speaker_one_text,
                speaker_two_text,
                speaker_one_id,
                voice_two_id,
                topic,
                num_turns,
            )

            # print("id one and url two")

        print("Speaker One Text:", speaker_one_text)
        print("Speaker Two Text:", speaker_two_text)
        print("Topic:", topic)
        print("Number of Turns:", num_turns)
        print("Speaker One URL:", speaker_one_url)
        print("Speaker Two URL:", speaker_two_url)
        print(speaker_one_id)
        print(speaker_two_id)
        print("Speaker One Voice Description:", speaker_one_voice_description)
        print("Speaker Two Voice Description:", speaker_two_voice_description)

        # Return a response or redirect to another page
        return render_template("download.html")

    return render_template("index1.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=5005)
