from fastapi import FastAPI
from agent_de_ia.app.api_endpoints import messages, audio

app = FastAPI(
    title="Agente de Acompanhamento",
    description="API para organização de registros e relatórios diários.",
    version="1.0.0"
)

app.include_router(
    messages.router,
    prefix="/api/v1",
    tags=["Messages"]
)

app.include_router(
    audio.router,
    prefix="/api/v1",
    tags=["Audio"]
)


@app.get("/")
def home():
    return {
        "message": "Agente de acompanhamento ativo!",
        "status": "online"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
