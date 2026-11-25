from fastapi import FastAPI
from agent_de_ia.app.api_endpoints import messages, audio
from agent_de_ia.app.api_endpoints import messages, audio, interpretations
from pathlib import Path
from fastapi.responses import FileResponse

app = FastAPI(
    title="Agente de Acompanhamento",
    description="API para organização de registros e relatórios diários.",
    version="1.0.0"
)

@app.get("/test", include_in_schema=False)
def test_interface():
    html_path = Path(__file__).resolve().parent / "static" / "test.html"
    return FileResponse(html_path)

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

app.include_router(
    interpretations.router,
    prefix="/api/v1",
    tags=["Interpretations"]
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
