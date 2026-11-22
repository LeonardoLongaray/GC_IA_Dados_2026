
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from agent_de_ia.app.schemas.audio_schema import AudioResponse

router = APIRouter()

# Formatos de áudio aceitos inicialmente
ALLOWED_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".m4a",
    ".ogg",
    ".opus",
    ".webm",
    ".flac"
}

# Limite definido para nosso endpoint: 20 MB
MAX_AUDIO_SIZE = 20 * 1024 * 1024


@router.post(
    "/audio",
    response_model=AudioResponse,
    status_code=202
)
async def receive_audio(
    patient_id: str = Form(...),
    caregiver_id: str = Form(...),
    file: UploadFile = File(...)
):
    filename = file.filename or "audio"

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail="Formato de áudio não suportado."
        )

    audio_content = await file.read(MAX_AUDIO_SIZE + 1)

    if not audio_content:
        raise HTTPException(
            status_code=400,
            detail="O arquivo de áudio está vazio."
        )

    if len(audio_content) > MAX_AUDIO_SIZE:
        raise HTTPException(
            status_code=413,
            detail="O áudio ultrapassa o limite de 20 MB."
        )

    response = AudioResponse(
        patient_id=patient_id,
        caregiver_id=caregiver_id,
        filename=filename,
        content_type=file.content_type,
        size_bytes=len(audio_content),
        received_at=datetime.now(timezone.utc),
        source="audio",
        status="received"
    )

    await file.close()

    return response
