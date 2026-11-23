
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


# Localiza o .env na raiz do projeto
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


MODEL = "whisper-large-v3"


def transcribe_audio(audio_bytes: bytes, filename: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY não configurada.")

    client = Groq(api_key=api_key)

    transcription = client.audio.transcriptions.create(
        file=(filename, audio_bytes),
        model=MODEL,
        language="pt",
        response_format="json",
        temperature=0.0
    )

    return transcription.text
