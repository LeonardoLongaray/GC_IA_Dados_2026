from datetime import datetime, timezone
from agent_de_ia.app.core.timezone import now_brasilia
from fastapi import APIRouter

from agent_de_ia.app.schemas.message_schemas import (
    MessageInput,
    MessageResponse
)

router = APIRouter()

@router.post("/messages",
    response_model=MessageResponse,
    status_code=202)
def receive_message(data: MessageInput):

    response = MessageResponse(
        patient_id=data.patient_id,
        caregiver_id=data.caregiver_id,
        original_message=data.message,
        received_at=now_brasilia(),
        source="text",
        status="received"
    )

    return response
