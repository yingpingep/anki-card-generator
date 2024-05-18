import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')

from pathlib import Path
from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

speech_file_path = Path(__file__).parent / "speech.mp3"
with client.audio.with_streaming_response.speech.create(
    model="tts-1",
    voice="alloy",
    input="test"
) as resp:
    resp.stream_to_file(speech_file_path)
