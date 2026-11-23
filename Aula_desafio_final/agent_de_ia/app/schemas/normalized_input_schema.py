from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field


class NormalizedInput(BaseModel):
    patient_id: str
    caregiver_id: str

    # Indica de onde veio a informação.
    source: Literal["text", "audio"]

    # Texto original ou texto transcrito.
    content: str = Field(min_length=1)

    # Momento em que a entrada foi recebida.
    received_at: datetime

    # Metadados opcionais do arquivo de áudio.
    original_filename: str | None = None
    content_type: str | None = None
    size_bytes: int | None = None
