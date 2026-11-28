from datetime import datetime
from pydantic import BaseModel

# Cria o objeto visual de modelo de resposta para áudio.
class AudioResponse(BaseModel):
    patient_id: str
    caregiver_id: str
    filename: str
    content_type: str | None
    size_bytes: int
    received_at: datetime
    source: str
    status: str
    transcription_text: str