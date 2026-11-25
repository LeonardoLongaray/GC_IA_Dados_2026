
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from starlette.concurrency import run_in_threadpool

from agent_de_ia.app.schemas.normalized_input_schema import NormalizedInput

from agent_de_ia.app.services.transcription_service import transcribe_audio

from agent_de_ia.app.services.normalization_service import normalize_audio


router = APIRouter()


# Extensões de áudio aceitas pelo sistema.
ALLOWED_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".m4a",
    ".ogg",
    ".opus",
    ".webm",
    ".flac"
}


# Tamanho máximo permitido: 20 MB.
MAX_FILE_SIZE = 20 * 1024 * 1024


@router.post(
    "/audio",
    response_model=NormalizedInput,
    status_code=200
)
async def receive_audio(
    patient_id: str = Form(...),
    caregiver_id: str = Form(...),
    file: UploadFile = File(...)
):

    received_at = datetime.now(timezone.utc)

    try:

        # 1. Verifica se o arquivo possui nome e extensão válidos.

        filename = file.filename or "audio.webm"

        extension = Path(filename).suffix.lower()

        if extension not in ALLOWED_EXTENSIONS:

            raise HTTPException(
                status_code=400,
                detail="Formato de áudio não permitido."
            )


        # 2. Lê o arquivo recebido.

        audio_bytes = await file.read()

        content_type = file.content_type

        if not audio_bytes:

            raise HTTPException(
                status_code=400,
                detail="O arquivo de áudio está vazio."
            )


        # 3. Verifica o tamanho do arquivo.

        size_bytes = len(audio_bytes)

        if size_bytes > MAX_FILE_SIZE:

            raise HTTPException(
                status_code=413,
                detail="O áudio ultrapassou o limite de 20 MB."
            )


        # 4. Envia o áudio para o serviço de transcrição.

        transcription_text = await run_in_threadpool(
            transcribe_audio,
            audio_bytes,
            filename
        )


        # 5. Verifica se a transcrição retornou algum conteúdo.

        if not transcription_text or not transcription_text.strip():

            raise HTTPException(
                status_code=422,
                detail="Não foi possível identificar uma fala no áudio."
            )


        # 6. Normaliza a transcrição.

        normalized_data = normalize_audio(
            patient_id=patient_id,
            caregiver_id=caregiver_id,
            transcription_text=transcription_text,
            filename=filename,
            content_type=content_type,
            size_bytes=size_bytes,
            received_at=received_at
        )


        # 7. Retorna os dados normalizados para a interface.

        return normalized_data


    except HTTPException:

        raise


    except RuntimeError as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


    except Exception:

        raise HTTPException(
            status_code=502,
            detail="Não foi possível realizar a transcrição do áudio."
        )


    finally:

        await file.close()
