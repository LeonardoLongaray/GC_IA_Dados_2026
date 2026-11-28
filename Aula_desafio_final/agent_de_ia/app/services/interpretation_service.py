import json
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from agent_de_ia.app.schemas.normalized_input_schema import NormalizedInput
from agent_de_ia.app.schemas.interpretation_schema import InterpretationResponse

# Busca o caminho do arquivo .env na raiz do projeto e carrega as variáveis de ambiente.
BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH, override=True)

# Diagnóstico de sistema, se encontrou ou não a chave e o modelo do GROQ.
print("================================")
print("DIAGNÓSTICO GROQ")
print("Raiz:", BASE_DIR)
print("Caminho .env:", ENV_PATH)
print("Arquivo encontrado:", ENV_PATH.exists())
print("Chave carregada:", bool(os.getenv("GROQ_API_KEY")))
print("Modelo carregado:", bool(os.getenv("GROQ_MODEL")))
print("================================")

# Prompt que é enviado ao Groq
SYSTEM_PROMPT = """
Você é um sistema de organização de relatos de cuidadores.

Sua função é extrair informações objetivas de relatos sobre
o acompanhamento de pacientes.

IDIOMA:
- Responda sempre em português brasileiro.
- Nunca traduza as observações para inglês ou outro idioma.

REGRAS OBRIGATÓRIAS:

1. Não faça diagnósticos.
2. Não recomende tratamentos ou alterações de medicamentos.
3. Não invente informações.
4. Não transforme suposições em fatos.
5. Preserve o sentido original do relato.
6. Só informe horários quando forem mencionados.
7. Se uma informação não estiver presente, não a invente.
8. Separe observações diferentes em itens diferentes.
9. Cada observação deve conter um trecho original que a sustente.
10. Não conclua que houve melhora ou piora clínica.
11. Preserve quantidades e unidades mencionadas.
12. Diferencie horário exato de período aproximado.

HORÁRIOS:
- Horários exatos devem ser preservados ou padronizados.
- "Pela manhã" deve ser registrado como "manhã".
- "Durante a tarde" deve ser registrado como "tarde".
- Nunca transforme períodos aproximados em horários exatos.

CATEGORIAS PERMITIDAS:
general, feeding, hydration, mobility, positioning, sleep,
elimination, skin_hygiene, medication, vital_signs, incident, other.

CLASSIFICAÇÃO DAS CATEGORIAS:

- general: estado geral, comportamento, disposição,
  sonolência e queixas relatadas, incluindo ausência
  de queixas de dor.
- feeding: alimentação.
- hydration: ingestão de líquidos.
- mobility: mobilidade e transferência.
- positioning: posicionamento.
- sleep: sono e períodos de descanso.
- elimination: eliminações.
- skin_hygiene: pele, higiene e feridas.
- medication: medicamentos administrados, conforme relato.
- vital_signs: sinais vitais efetivamente medidos.
- incident: intercorrências relatadas.
- other: informações que não se encaixam nas demais categorias.

INFORMAÇÕES AUSENTES:
- Liste somente informações relevantes para compreender
  as observações relatadas.
- Não invente dados ausentes.
- Não crie pendências sem justificativa.

Responda exclusivamente com JSON válido, seguindo esta estrutura:

{
    "observations": [
        {
            "category": "feeding",
            "description": "O paciente consumiu metade do pão.",
            "reported_time": "08:00",
            "evidence_text": "comeu apenas metade do pão"
        }
    ],
    "missing_information": [],
    "review_required": true
}

Não inclua explicações fora do JSON.
"""

# Função que interpreta a entrada do usuário usando o modelo Groq.
def interpret_input(data: NormalizedInput) -> InterpretationResponse:
    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv("GROQ_MODEL")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY não configurada.")
    
    if not model:
        raise RuntimeError("GROQ_MODEL não configurado.")

    client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key,
    timeout=60.0)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": data.content
            }
        ],
        response_format={"type": "json_object"},
        temperature=0
    )

    result_text = response.choices[0].message.content

    if not result_text:
        raise ValueError("O modelo retornou uma resposta vazia.")

    result_json = json.loads(result_text)

    return InterpretationResponse(
        patient_id=data.patient_id,
        caregiver_id=data.caregiver_id,
        source=data.source,
        received_at=data.received_at,
        **result_json
    )
