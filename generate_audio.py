import requests
import io, os, re

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

XI_API_KEY = os.getenv("XI_API_KEY")
arlin_voice_id = os.getenv("ARLIN_VOICE_ID")
# ariana_voice_id = os.getenv("ARIANA_VOICE_ID")

def get_audio(text, filename):
    # Name the file by the first 3 words in the text
    file_name = text.split(" ")
    if len(file_name) > 3:
        file_name = "_".join(file_name[:3])
    else:
        file_name = "_".join(file_name)

    # print("Prompt")
    # print(text)
    file_name = re.sub('[^A-Za-z0-9]+', '_', file_name).strip('_')

    options = {
        'headers': {
            'accept': '*/*',
            'Content-Type': 'application/json',
            'xi-api-key': XI_API_KEY,
        },
        'json': {
            'text': text,
            'voice_settings': {
                'stability': 0.75,
                'similarity_boost': 0.75,
            }
        },
    }

    try:
        response = requests.post(f'https://api.elevenlabs.io/v1/text-to-speech/{arlin_voice_id}', **options)
        # response = requests.post(f'https://api.elevenlabs.io/v1/text-to-speech/{ariana_voice_id}', **options)
        audio_dir = 'audio'
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)

        arr = []
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                arr.append(chunk)

        buffered_data = b''.join(arr)
        with io.BytesIO(buffered_data) as f:
            with open(f"{audio_dir}/{filename}", "wb") as audio_file:
                audio_file.write(f.read())
        
        print("Audio written to file as", file_name)

    except Exception as e:
        print(e)
        return None

    # return buffered_data