from datetime import datetime, timezone
from pydantic import BaseModel, Field

# Cria o objeto visual para as mensagens

class MessageInput(BaseModel):
    patient_id: str = Field(
        min_length=1,
        description="Identificador do paciente"
    )

# Define o ID do cuidador
    caregiver_id: str = Field(
        min_length=1,
        description="Identificador do cuidador"
    )

# Define o relato escrito do cuidador
    message: str = Field(
        min_length=1,
        max_length=5000,
        description="Relato escrito do cuidador"
    )

# Define o objeto visual das informações recebidas
class MessageResponse(BaseModel):
    patient_id: str
    caregiver_id: str
    original_message: str
    received_at: datetime
    source: str
    status: str
