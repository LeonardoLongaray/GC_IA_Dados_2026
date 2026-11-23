from fastapi import APIRouter, HTTPException
from starlette.concurrency import run_in_threadpool
from agent_de_ia.app.schemas.normalized_input_schema import NormalizedInput
from agent_de_ia.app.schemas.interpretation_schema import InterpretationResponse
from agent_de_ia.app.services.interpretation_service import interpret_input


router = APIRouter()


@router.post(
    "/interpretations",
    response_model=InterpretationResponse,
    status_code=200
)
async def create_interpretation(data: NormalizedInput):

    try:
        result = await run_in_threadpool(
            interpret_input,
            data
        )

        return result

    except RuntimeError as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Não foi possível interpretar o relato."
        )
