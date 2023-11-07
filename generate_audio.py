import openai
import requests
import time
from pydub import AudioSegment
import os

# from pytube import YouTube
from moviepy.editor import *
import requests
from api_key import api_openai_key, eleven_labs_api


eleven_labs_api_key = eleven_labs_api
openai.api_key = api_openai_key


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
    full_audio = None
    # transcript_text = None

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
                filename = f"Url_Audio/{name}_turn_{i}.mp3"
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
                filename = f"Url_Audio/{name}_turn_{i}.mp3"
                with open(filename, "wb") as f:
                    for chunk in tts_response.iter_content(chunk_size=CHUNK_SIZE):
                        if chunk:
                            f.write(chunk)

            time.sleep(3)  # Delay to ensure the file is written to disk

            # Concatenate audio
            pause = AudioSegment.silent(duration=100)
            # 100ms pause
            # print("1111", filename)
            new_audio = AudioSegment.from_mp3(filename)
            full_audio = full_audio + new_audio + pause if full_audio else new_audio
            """except:
                new_audio = AudioSegment.from_mp3(f"Url_Audio/{filename}")
                full_audio = full_audio + new_audio + pause if full_audio else new_audio
                print("222", filename)"""

        if i == num_turns - 1:  # Last turn
            wrap_up_message = {
                "role": "system",
                "content": "This is your last turn to speak, wrap it up.",
            }
            conversation_history.append(wrap_up_message)

    with open(f"Podcast_textfile/Podcast_Transcript.txt", "w") as text1:
        text1.write(transcript_text)
    # Export full audio
    full_audio.export("Final_Audio/podcast.mp3", format="mp3")


"""generate_podcast(
    "ANURAG RAI",
    "SHIVAM RAI",
    "vJugPFXI9NE4lH1rzobg",
    "reoU0XsX7sIfwjTFNgeM",
    "MACHINE LEARNING",
    7,
)
"""
