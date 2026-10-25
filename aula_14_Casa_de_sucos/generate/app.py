
import requests
from urllib.parse import quote
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="API Casa de Sucos")

BASE_URL = "https://www.fruityvice.com/api/fruit"

# Armazenamento temporário dos sucos
sucos = []
proximo_id = 1


# Modelo dos dados recebidos ao criar um suco
class SucoEntrada(BaseModel):
    nome: str = Field(min_length=1)
    frutas: list[str] = Field(min_length=1)
    tem_gosto_de: str = Field(min_length=1)


# Modelo dos dados recebidos ao atualizar as frutas
class AtualizarFrutas(BaseModel):
    frutas: list[str] = Field(min_length=1)


def consultar_fruta(nome: str):
    """Consulta uma fruta na API Fruityvice."""

    nome_url = quote(nome.strip().lower(), safe="")

    try:
        response = requests.get(
            f"{BASE_URL}/{nome_url}",
            timeout=10
        )
    except requests.RequestException:
        raise HTTPException(
            status_code=502,
            detail="Não foi possível acessar a API Fruityvice."
        )

    if response.status_code == 404:
        return None

    try:
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError):
        raise HTTPException(
            status_code=502,
            detail="A API Fruityvice retornou uma resposta inválida."
        )


def calcular_totais(frutas: list[str]):
    """Consulta as frutas e soma calorias e açúcar."""

    total_calorias = 0
    total_acucar = 0

    for nome_fruta in frutas:
        fruta = consultar_fruta(nome_fruta)

        if fruta is None:
            raise HTTPException(
                status_code=404,
                detail=f"A fruta '{nome_fruta}' não foi encontrada."
            )

        nutrientes = fruta["nutritions"]

        total_calorias += nutrientes["calories"]
        total_acucar += nutrientes["sugar"]

    return {
        "total_calorias": round(total_calorias, 2),
        "total_acucar": round(total_acucar, 2)
    }


# GET /frutas/{nome}
@app.get("/frutas/{nome}")
def obter_fruta(nome: str):
    fruta = consultar_fruta(nome)

    if fruta is None:
        raise HTTPException(
            status_code=404,
            detail=f"A fruta '{nome}' não foi encontrada."
        )

    nutrientes = fruta["nutritions"]

    return {
        "nome": fruta["name"],
        "calorias": nutrientes["calories"],
        "acucar": nutrientes["sugar"]
    }


# POST /sucos
@app.post("/sucos", status_code=201)
def criar_suco(dados: SucoEntrada):
    global proximo_id

    nome = dados.nome.strip()
    frutas = [fruta.strip().lower() for fruta in dados.frutas]

    if not nome or not dados.tem_gosto_de.strip():
        raise HTTPException(
            status_code=422,
            detail="O nome do suco e o sabor preferido são obrigatórios."
        )

    if any(not fruta for fruta in frutas):
        raise HTTPException(
            status_code=422,
            detail="Os nomes das frutas não podem estar vazios."
        )

    totais = calcular_totais(frutas)

    suco = {
        "id": proximo_id,
        "nome": nome,
        "frutas": frutas,
        "tem_gosto_de": dados.tem_gosto_de.strip(),
        **totais
    }

    sucos.append(suco)
    proximo_id += 1

    return suco


# GET /sucos
@app.get("/sucos")
def listar_sucos():
    return sucos


# PUT /sucos/{id}
@app.put("/sucos/{id}")
def atualizar_suco(id: int, dados: AtualizarFrutas):
    frutas = [fruta.strip().lower() for fruta in dados.frutas]

    if any(not fruta for fruta in frutas):
        raise HTTPException(
            status_code=422,
            detail="Os nomes das frutas não podem estar vazios."
        )

    suco_encontrado = None

    for suco in sucos:
        if suco["id"] == id:
            suco_encontrado = suco
            break

    if suco_encontrado is None:
        raise HTTPException(
            status_code=404,
            detail="Suco não encontrado."
        )

    # Calcula os novos totais antes de alterar o cadastro
    totais = calcular_totais(frutas)

    suco_encontrado["frutas"] = frutas
    suco_encontrado.update(totais)

    return suco_encontrado
