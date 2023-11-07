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
    voice_id = "Voice_Id_File/generated_voice_id.txt"  # Path to your .txt file
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


"""
def generate_podcast(name1, name2, name1_voice, name2_voice, topic, num_turns):
    conversation_history = []
    system_prompt1 = {
        "role": "system",
        "content": f"You are {name1}. You are recording a podcast with {name2} about {topic}. Talk as naturally as possible -- use the language {name1} would actually use. Don't just blindly agree — debate, discuss, and have fun! Respond with one message per turn. Don't include anything other than your response.",
    }
    system_prompt2 = {
        "role": "system",
        "content": f"You are {name2}. You are recording a podcast with {name1} about {topic}. Talk as naturally as possible -- use the language {name2} would actually use. Don't just blindly agree — debate, discuss, and have fun! Respond with one message per turn. Don't include anything other than your response.",
    }

    transcript_text = ""
    transcript_text = None

    for i in range(num_turns):  # Limit the conversation to 5 turns for each character
        for name, system_prompt in [(name1, system_prompt1), (name2, system_prompt2)]:
            try:
                # Adjust the role of each speaker in the conversation history
                adjusted_history = [
                    {
                        "role": "assistant" if msg["role"] == name else "user",
                        "content": msg["content"],
                    }
                    for msg in conversation_history
                ]
                adjusted_history.append(system_prompt)
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=adjusted_history,
                    presence_penalty=0.7,
                )
                message = response.choices[0].message["content"]

                print(f"{name}: {message}")
                transcript_text += f"{name}: {message}\n\n"

                conversation_history.append({"role": name, "content": message})
            except:
                time.sleep(30)
                # Adjust the role of each speaker in the conversation history
                adjusted_history = [
                    {
                        "role": "assistant" if msg["role"] == name else "user",
                        "content": msg["content"],
                    }
                    for msg in conversation_history
                ]
                adjusted_history.append(system_prompt)
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=adjusted_history,
                    presence_penalty=0.7,
                )
                message = (
                    response.choices[0]
                    .message["content"]
                    .replace("*(burps)*", "")
                    .replace("*(laughs)*", "")
                    .replace("*laughs and burps*", "")
                    .replace("*belches and laughs*", "")
                )
                print(f"{name}: {message}")
                transcript_text += f"{name}: {message}\n\n"
                conversation_history.append({"role": name, "content": message})

            if name == name1:
                voice = name1_voice
            else:
                voice = name2_voice

            # Generate and save audio for the message
            try:
                CHUNK_SIZE = 1024
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"
                headers = {
                    "Accept": "audio/mpeg",
                    "Content-Type": "application/json",
                    "xi-api-key": eleven_labs_api_key,
                }
                data = {
                    "text": message,
                    "model_id": "eleven_monolingual_v1",
                    "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
                }
                tts_response = requests.post(url, json=data, headers=headers)
                filename = f"{name}_turn_{i}.mp3"
                with open(filename, "wb") as f:
                    for chunk in tts_response.iter_content(chunk_size=CHUNK_SIZE):
                        if chunk:
                            f.write(chunk)
            except:
                time.sleep(30)
                CHUNK_SIZE = 1024
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"
                headers = {
                    "Accept": "audio/mpeg",
                    "Content-Type": "application/json",
                    "xi-api-key": eleven_labs_api_key,
                }
                data = {
                    "text": message,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {"stability": 0.7, "similarity_boost": 0.75},
                }
                tts_response = requests.post(url, json=data, headers=headers)
                filename = f"{name}_turn_{i}.mp3"
                with open(filename, "wb") as f:
                    for chunk in tts_response.iter_content(chunk_size=CHUNK_SIZE):
                        if chunk:
                            f.write(chunk)

            time.sleep(3)  # Delay to ensure the file is written to disk

            # Concatenate audio
            pause = AudioSegment.silent(duration=100)  # 100ms pause
            new_audio = AudioSegment.from_mp3(filename)
            full_audio = full_audio + new_audio + pause if full_audio else new_audio

        if i == num_turns - 1:  # Last turn
            wrap_up_message = {
                "role": "system",
                "content": "This is your last turn to speak, wrap it up.",
            }
            conversation_history.append(wrap_up_message)

    with open(f"Podcast_textfile/{topic}_Podcast_Transcript.txt", "w") as text1:
        text1.write(transcript_text)
    # Export full audio
    full_audio.export("podcast.mp3", format="mp3")

    # Play the audio in the notebook
    # return "file is created successfully"  # Audio("podcast.mp3")
"""

"""def download_and_trim_audio(clip_url, filename, max_size):
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
        print(f"Trimmed: {initial_duration - final_duration:.2f} seconds")"""


"""def upload_to_api(filename, name, description, api_key):
    url = "https://api.elevenlabs.io/v1/voices/add"
    headers = {
        "Accept": "application/json",
        "xi-api-key": api_key,
    }
    data = {
        "name": name,
        "labels": '{"accent": "American"}',
        "description": description,
    }
    files = [
        ("files", (f"{filename}.mp3", open(f"{filename}.mp3", "rb"), "audio/mpeg")),
    ]
    response = requests.post(url, headers=headers, data=data, files=files)
    print(response.json())
    return response.json()["voice_id"]"""


def save_voice_id(id_1, id_2):
    with open("Voice_id_File/generated_voice_id.txt", "w") as voiceid:
        voiceid.write(f"speaker one voice id: {id_1} \n speaker two voice id: {id_2}")


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

        if speaker_one_url is not None and speaker_two_url is not None:
            print("both url")

        # if speaker_one_id is not None and speaker_two_id is not None:
        if speaker_one_id is not None and speaker_two_id is not None:
            print("both id")

        if speaker_one_url is not None and speaker_two_id is not None:
            print("url one and id two")

        if speaker_one_id is not None and speaker_two_url is not None:
            print("id one and url two")
        # Now you can use the collected information as needed for further processing
        # For example, you can print or store these values in a database.

        # Example of printing the collected information:
        print("Speaker One Text:", speaker_one_text)
        print("Speaker Two Text:", speaker_two_text)
        print("Topic:", topic)
        print("Number of Turns:", num_turns)
        print("Speaker One ID:", speaker_one_id)
        print("Speaker One URL:", speaker_one_url)
        print("Speaker Two ID:", speaker_two_id)
        print("Speaker Two URL:", speaker_two_url)
        print("Speaker One Voice Description:", speaker_one_voice_description)
        print("Speaker Two Voice Description:", speaker_two_voice_description)

        # You can add your processing logic here.

    return render_template("index1.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
