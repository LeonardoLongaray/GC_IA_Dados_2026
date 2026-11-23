from datetime import datetime, timezone
from agent_de_ia.app.schemas.normalized_input_schema import (
    NormalizedInput
)


def normalize_message(
    patient_id: str,
    caregiver_id: str,
    message: str
) -> NormalizedInput:

    # Organiza uma mensagem escrita no formato padrão.
    return NormalizedInput(
        patient_id=patient_id,
        caregiver_id=caregiver_id,
        source="text",
        content=message,
        received_at=datetime.now(timezone.utc)
    )


def normalize_audio(
    patient_id: str,
    caregiver_id: str,
    transcription_text: str,
    filename: str,
    content_type: str | None,
    size_bytes: int,
    received_at: datetime
) -> NormalizedInput:

    # Organiza a transcrição e preserva os metadados do áudio.
    return NormalizedInput(
        patient_id=patient_id,
        caregiver_id=caregiver_id,
        source="audio",
        content=transcription_text,
        received_at=received_at,
        original_filename=filename,
        content_type=content_type,
        size_bytes=size_bytes
    )
