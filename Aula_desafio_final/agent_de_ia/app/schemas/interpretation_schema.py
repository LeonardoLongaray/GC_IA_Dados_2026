from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field

# Cria o objeto visual de modelo das categorias e quadros de descrição para interpretação.

class Observation(BaseModel):
    category: Literal[
        "general",
        "feeding",
        "hydration",
        "mobility",
        "positioning",
        "sleep",
        "elimination",
        "skin_hygiene",
        "medication",
        "vital_signs",
        "incident",
        "other"
    ]

    description: str = Field(
        min_length=1,
        description="Descrição objetiva do que foi relatado"
    )

    reported_time: str | None = None

    evidence_text: str = Field(
        min_length=1,
        description="Trecho original que sustenta a observação"
    )

# Aplica um molde visual das interpretações

class InterpretationResponse(BaseModel):
    patient_id: str
    caregiver_id: str
    source: Literal["text", "audio"]
    received_at: datetime

    observations: list[Observation]

    missing_information: list[str] = []

    review_required: bool = True
