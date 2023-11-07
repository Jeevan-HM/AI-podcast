import requests


def upload_to_api(filename, name, description, api_key):
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
    return response.json()["voice_id"]
