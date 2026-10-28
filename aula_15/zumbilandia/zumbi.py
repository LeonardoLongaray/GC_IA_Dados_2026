from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

filmes = [{"id": 1, "titulo": "A Última Meia-Noite"}]


class NovoFilme(BaseModel):
    titulo: str
    nota: float


@app.get("/")
def inicio():
    return {"mensagem": "Oi"}


@app.get("/filmes")
def listar_filmes():
    return filmes


@app.get("/filmes/{filme_id}")
def buscar_filme(filme_id: int):
    return {"id": filme_id}


@app.post("/filmes")
def adicionar_filme(novo: NovoFilme):
    return novo.model_dump()