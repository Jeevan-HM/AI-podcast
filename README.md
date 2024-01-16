# AI Podcast

Welcome to the AI Podcast repository! This project is all about generating simulated podcast conversations between two characters using text-to-speech and AI language models. It's like having your own personal podcast studio, right at your fingertips! 🎧

## Table of Contents 📚

1. [Requirements](#requirements)
2. [Files](#files)
3. [Usage](#usage)
4. [Notes](#notes)

## Requirements 🛠️

This project relies on several Python dependencies, all of which are listed in the `requirements.txt` file. Some of the major ones include `aiohttp`, `Flask`, `numpy`, `openai`,'`eleven labs` `pydantic`, `requests`, and `websockets` among others. To install all the dependencies, use the following command:

```bash
pip install -r requirements.txt
```

## Files 📂

Here's a quick rundown of the main files in this repository and what they do:

- `elevenlabs_api.py`: Uploads audio files to the Eleven Labs API. 📤
- `url_video.py`: Downloads and trims audio from a YouTube video. 🎥
- `generate_audio.py`: Generates a simulated podcast conversation. 🗣️
- `app.py`: A Flask application that allows users to generate a podcast using text inputs and voice samples. 🌐
- `index.html`: An HTML form for the AI Podcast. 📝
- `app1.py`: Another Flask application for generating a podcast conversation. 🌐
- `generated_voice_id.txt`: Stores the voice IDs for two speakers. 🆔
- `download.html`: A webpage that allows users to download various files. ⬇️
- `index1.html`: Another HTML form for the AI Podcast. 📝

## Usage 💻

Here's a quick example of how you might use some of the Python files in this repository:

```python
# Create a .env file and add your 'openai' and 'elevenlabs' api key 

api_openai_key= 
eleven_labs_api= 

# Then run the command below
```

```bash
python3 app.py
```

## Notes 📝

- Ensure that the environment variables "api_openai_key" and "eleven_labs_api" are set in your system before running this file.
- The function prints the response from the API and returns the 'voice_id' of the uploaded file which can be used in the future to retrieve the voice.

Happy podcasting! 🎉