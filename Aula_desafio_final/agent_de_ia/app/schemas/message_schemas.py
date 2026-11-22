from datetime import datetime, timezone
from pydantic import BaseModel, Field

### Edita as informações que chegam na API

class MessageInput(BaseModel):
    patient_id: str = Field(
        min_length=1,
        description="Identificador do paciente"
    )

    caregiver_id: str = Field(
        min_length=1,
        description="Identificador do cuidador"
    )

    message: str = Field(
        min_length=1,
        max_length=5000,
        description="Relato escrito do cuidador"
    )


class MessageResponse(BaseModel):
    patient_id: str
    caregiver_id: str
    original_message: str
    received_at: datetime
    source: str
    status: str
