
from datetime import datetime, timezone
from pathlib import Path

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException
)
from starlette.concurrency import run_in_threadpool

from agent_de_ia.app.schemas.audio_schema import AudioResponse
from agent_de_ia.app.services.transcription_service import (
    transcribe_audio
)


router = APIRouter()

ALLOWED_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".m4a",
    ".ogg",
    ".opus",
    ".webm",
    ".flac"
}

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

    try:
        transcription_text = await run_in_threadpool(
            transcribe_audio,
            audio_content,
            filename
        )

    except RuntimeError:
        raise HTTPException(
            status_code=500,
            detail="Configuração da transcrição indisponível."
        )

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Não foi possível realizar a transcrição."
        )

    finally:
        await file.close()

    if not transcription_text.strip():
        raise HTTPException(
            status_code=422,
            detail="Não foi possível identificar fala no áudio."
        )

    return AudioResponse(
        patient_id=patient_id,
        caregiver_id=caregiver_id,
        filename=filename,
        content_type=file.content_type,
        size_bytes=len(audio_content),
        received_at=datetime.now(timezone.utc),
        source="audio",
        status="transcribed",
        transcription_text=transcription_text
    )