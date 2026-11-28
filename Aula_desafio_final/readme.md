# Agente de Acompanhamento

Backend em **FastAPI** para receber relatos de cuidadores por texto ou
áudio, transcrever gravações e organizar observações com auxílio de IA.
------------------------------------------------------------------------
## Inicialização rápida --- Windows CMD

A partir da raiz `Aula_desafio_final`:

``` cmd
cd agent_de_ia
.venv\Scripts\activate.bat
cd ..
python -m uvicorn agent_de_ia.app.main:app --reload
```

Antes de iniciar, confirme que `agent_de_ia/.env` contém `GROQ_API_KEY`
e `GROQ_MODEL`.

-   Swagger: http://127.0.0.1:8000/docs
-   Interface: http://127.0.0.1:8000/test
------------------------------------------------------------------------

## Índice

1.  [Visão geral](#1-visão-geral)
2.  [Tecnologias](#2-tecnologias)
3.  [Pré-requisitos](#3-pré-requisitos)
4.  [Estrutura do projeto](#4-estrutura-do-projeto)
5.  [Ambiente virtual](#5-ambiente-virtual)
6.  [Dependências](#6-dependências)
7.  [Variáveis de ambiente e APIKey](#7-variáveis-de-ambiente-e-api-key)
8.  [Executar o agente](#8-executar-o-agente)
9.  [Endpoints](#9-endpoints)
10. [Categorias](#11-categorias)
11. [Solução de problemas](#12-solução-de-problemas)

------------------------------------------------------------------------

## 1. Visão geral

O Agente de Acompanhamento recebe relatos de cuidadores sobre pessoas
acompanhadas. As entradas podem ser mensagens digitadas ou gravações de
áudio.

**Objetivo:** apoiar a organização de informações para revisão por
profissionais responsáveis. O sistema não diagnostica, não prescreve e
não substitui avaliação profissional.

## 2. Tecnologias

  Tecnologia                    Utilização
  ----------------------------- ----------------------------------------------
  Python                        Linguagem do backend
  FastAPI                       Construção da API
  Uvicorn                       Servidor ASGI
  Pydantic                      Validação dos dados
  python-dotenv                 Leitura do `.env`
  Groq SDK                      Integração com serviço de transcrição
  OpenAI Python SDK             Cliente compatível com a API de chat da Groq
  Whisper `whisper-large-v3`    Transcrição de áudio
  GPT-OSS configurado na Groq   Interpretação dos relatos
  HTML, CSS e JavaScript        Interface de testes
  MediaRecorder API             Gravação pelo navegador

## 3. Pré-requisitos

-   Python 3.10 ou superior, em versão compatível com as dependências.
-   VS Code ou editor equivalente.
-   Git (se for clonar/versionar o projeto).
-   Navegador moderno para testar a interface e o microfone.
-   Conta e API Key da Groq.

Verifique as instalações:

``` bash
python --version
pip --version
git --version
```

## 4. Estrutura do projeto

Estrutura de referência:

``` text
agent_de_ia/
|── .env
├── .env.example
├── .venv/
├── requirements.txt
└── app/
    ├── main.py
    ├── api_endpoints/
    │   |── messages.py
    │   ├── audio.py
    │   └── interpretations.py
    ├── schemas/
    │   ├── message_schema.py
    │   ├── normalized_input_schema.py
    │   └── interpretation_schema.py
    ├── services/
    │   ├── normalization_service.py
    │   ├── transcription_service.py
    │   └── interpretation_service.py
    |── core/
    |   └── timezone.py
    └── static/
        └── test.html
```

**Responsabilidades:** - `api/endpoints/`: rotas HTTP. - `schemas/`:
contratos e validação dos dados. - `services/`: normalização,
transcrição e interpretação. - `core/`: configurações compartilhadas. 
`static/`: html do ambiente de teste do agente -

## 5. Ambiente virtual

Abra o terminal na raiz do projeto e entre na pasta do backend:

``` cmd
cd agent_de_ia
```

Crie o ambiente virtual:

``` bash
python -m venv .venv
```

Ative no **Windows CMD**:

``` cmd
.venv\Scripts\activate.bat
```

Ou no **PowerShell**:

``` powershell
.\.venv\Scripts\Activate.ps1
```

Com o ambiente ativo, o terminal normalmente mostra `(.venv)`. O
ambiente virtual isola as bibliotecas Python deste projeto.

## 6. Dependências

Com `.venv` ativado, instale as dependências:

``` bash
pip install -r requirements.txt
```

Execute o comando dentro de `agent_de_ia`, onde está o arquivo
`requirements.txt`.

## 7. Variáveis de ambiente e API Key

A aplicação usa `.env` para guardar configurações locais e credenciais.
O arquivo deve ficar dentro de `agent_de_ia`, ao lado de `.venv` e
`requirements.txt`.

### 7.1 Criar o `.env`

Copie o `agent_de_ia/.env.exemple` alterando o nome para `.env`:

``` .env
GROQ_API_KEY=sua_chave_de_api_aqui
GROQ_MODEL=openai/gpt-oss-120b
```

Troque `sua_chave_de_api_aqui` pela chave da sua conta Groq. Não
compartilhe a chave, não a coloque no código e não envie o `.env` ao
Git.

### 7.2 Obter a API Key da Groq

1.  Acesse [Groq Console](https://console.groq.com/).
2.  Entre ou crie uma conta.
3.  Abra a seção **API Keys**.
4.  Crie uma chave e copie o valor apresentado.
5.  Cole no campo `GROQ_API_KEY` do `.env`.

Guarde a chave em local seguro. Se ela for exposta, revogue-a no console
e gere outra.

### 7.3 Modelo de interpretação

`GROQ_MODEL` configura o modelo de linguagem utilizado pelo serviço de
interpretação, desde que o código esteja lendo essa variável.

Modelo utilizado nos testes registrados:

``` env
GROQ_MODEL=openai/gpt-oss-120b
```

Para trocar de modelo, altere o identificador para outro atualmente
suportado pela Groq e reinicie a aplicação. Modelos, limites e
disponibilidade podem mudar; confira o console e a documentação do
provedor.

O modelo de transcrição é configurado separadamente no serviço de áudio:

``` python
MODEL = "whisper-large-v3"
```

### 7.4 `.env.example`

Mantenha um exemplo sem credenciais para orientar quem configurar o
projeto:

``` env
GROQ_API_KEY=
GROQ_MODEL=openai/gpt-oss-120b
```

O `.env.example` pode ser versionado; o `.env` real não.

### 7.5 `.gitignore`

Garanta que o `.gitignore` contenha:

``` gitignore
.venv/
.env
__pycache__/
*.py[cod]
.pytest_cache/
```

Não ignore `requirements.txt` nem `.env.example`.

## 8. Executar o agente

Com o ambiente virtual ativo, volte para a raiz `Aula_desafio_final`:

``` cmd
cd ..
```

Execute:

``` bash
python -m uvicorn agent_de_ia.app.main:app --reload
```

O comando acima deve ser executado a partir da raiz
`Aula_desafio_final`, conforme os imports utilizados no projeto.

### Endereços locais

  Recurso                             URL
  ----------------------------------- ------------------------------
  Página inicial da API               http://127.0.0.1:8000/
  Health check                        http://127.0.0.1:8000/health
  Swagger / documentação interativa   http://127.0.0.1:8000/docs
  Interface de testes                 http://127.0.0.1:8000/test

A rota `/test` depende de o `main.py` configurar o serviço da página
HTML/arquivos estáticos. Se retornar 404, confira a configuração e o
caminho real de `test.html`.

Para parar o servidor, pressione `CTRL + C`. O `--reload` reinicia o
servidor quando arquivos Python são alterados. Alterações no `.env`
podem exigir reinicialização manual.

## 9. Endpoints

Prefixo principal: `/api/v1`.

  ---------------------------------------------------------------------------
  Método                  Endpoint                    Função
  ----------------------- --------------------------- -----------------------
  `GET`                   `/`                         Mensagem inicial da
                                                      aplicação.

  `GET`                   `/health`                   Verifica se a API
                                                      responde.

  `POST`                  `/api/v1/messages`          Recebe e normaliza
                                                      relato escrito.

  `POST`                  `/api/v1/audio`             Recebe áudio,
                                                      transcreve e normaliza.

  `POST`                  `/api/v1/interpretations`   Interpreta uma entrada
                                                      normalizada.
  ---------------------------------------------------------------------------

### 9.1 `POST /api/v1/messages`

Recebe JSON:

``` json
{
  "patient_id": "PAC-001",
  "caregiver_id": "CUID-001",
  "message": "Hoje o paciente tomou café da manhã às oito horas."
}
```

A rota valida os campos e chama `normalize_message()`. O resultado é um
`NormalizedInput` com `source: "text"` e a mensagem em `content`.

### 9.2 `POST /api/v1/audio`

Recebe `multipart/form-data`, não JSON.

  Campo            Tipo         Descrição
  ---------------- ------------ ----------------------------
  `patient_id`     Form/texto   Identificador do paciente.
  `caregiver_id`   Form/texto   Identificador do cuidador.
  `file`           Arquivo      Arquivo de áudio.

O endpoint documentado no projeto prevê limite de 20 MB e extensões
`.wav`, `.mp3`, `.m4a`, `.ogg`, `.opus`, `.webm` e `.flac`.

Etapas: 1. Validar extensão e tamanho. 2. Ler o arquivo. 3. Chamar
`transcribe_audio()`. 4. Verificar se a transcrição não está vazia. 5.
Chamar `normalize_audio()`. 6. Retornar `NormalizedInput` com
`source: "audio"` e a transcrição em `content`.

O ponto essencial é `content`: ele precisa conter o texto transcrito
para ser encaminhado ao interpretador.

### 9.3 `POST /api/v1/interpretations`

Recebe um `NormalizedInput` em JSON:

``` json
{
  "patient_id": "PAC-001",
  "caregiver_id": "CUID-001",
  "source": "text",
  "content": "Hoje o paciente tomou café da manhã às oito horas.",
  "received_at": "2026-11-28T13:00:00Z"
}
```

A rota chama `interpret_input()`, que envia o conteúdo textual ao modelo
configurado na Groq e retorna uma estrutura `InterpretationResponse`.

O contrato de interpretação trabalhado inclui: - `patient_id`,
`caregiver_id`, `source` e `received_at`; - `observations`: observações
identificadas; - `missing_information`: informações pendentes
identificadas; - `review_required`: sinalização de revisão humana.

Cada observação pode conter categoria, descrição, horário relatado e
evidência textual. O campo `information_status` e os valores possíveis
dependem de estarem efetivamente presentes no schema e no prompt local.

## 10. Categorias

Os códigos internos podem permanecer em inglês; a interface apresenta
rótulos em português.

  -----------------------------------------------------------------------
  Código                  Nome apresentado        Conteúdo esperado
  ----------------------- ----------------------- -----------------------
  `general`               Estado geral            Comportamento,
                                                  disposição e queixas
                                                  relatadas.

  `feeding`               Alimentação             Refeições, aceitação e
                                                  recusa alimentar.

  `hydration`             Hidratação              Ingestão de água e
                                                  outros líquidos.

  `mobility`              Mobilidade              Movimentação e
                                                  transferências.

  `positioning`           Posicionamento          Mudanças e manutenção
                                                  de posição.

  `sleep`                 Sono e descanso         Sono, repouso e
                                                  despertares.

  `elimination`           Eliminações             Informações sobre
                                                  eliminações.

  `skin_hygiene`          Pele e higiene          Higiene, condição da
                                                  pele e feridas
                                                  relatadas.

  `medication`            Medicação               Registro do que foi
                                                  relatado como
                                                  administrado.

  `vital_signs`           Sinais vitais           Medições relatadas, com
                                                  valor, unidade e
                                                  horário quando
                                                  disponíveis.

  `incident`              Intercorrências         Quedas e outros eventos
                                                  relatados.

  `other`                 Outros registros        Informações que não se
                                                  encaixam nas demais
                                                  categorias.
  -----------------------------------------------------------------------

Ao alterar categorias, alinhe `interpretation_schema.py`, o prompt do
modelo e os rótulos da interface.

## 11 Solução de problemas

### `GROQ_API_KEY não configurada`

-   Confirme que `.env` está dentro de `agent_de_ia`.
-   Confira o nome `GROQ_API_KEY`.
-   Confira se a chave foi copiada corretamente.
-   Confira se o serviço carrega o `.env` pelo caminho correto.
-   Reinicie o servidor.

### Modelo indisponível ou `GROQ_MODEL` não carregado

-   Confira o valor de `GROQ_MODEL`.
-   Verifique se o modelo ainda é suportado pela Groq.
-   Confira limites e disponibilidade no console.
-   Reinicie a aplicação depois de alterar o `.env`.

### `body → content: Field required`

O endpoint de interpretação exige `content`. Confira se a interface
envia o texto nesse campo, seguindo o formato `NormalizedInput`.

### Endpoint de áudio não retornou texto transcrito

Confira: 1. Se `POST /api/v1/audio` recebeu o arquivo. 2. Se extensão e
tamanho são aceitos. 3. Se `transcribe_audio()` concluiu a transcrição.
4. Se `normalize_audio()` atribuiu `transcription_text` a `content`. 5.
Se a resposta JSON de `/audio` realmente contém `content`.

### Microfone não funciona

-   Autorize o acesso ao microfone no navegador.
-   Confira o dispositivo de entrada selecionado no sistema.
-   Feche aplicativos que possam estar utilizando o microfone.
-   Acesse por `localhost` ou `127.0.0.1`. Navegadores normalmente
    permitem microfone em contextos locais seguros.

### `/test` retorna 404

Confira se `main.py` configura a rota da interface/arquivos estáticos e
se `test.html` está no diretório esperado.

### Erro de importação

-   Ative `.venv`.
-   Execute Uvicorn a partir da raiz `Aula_desafio_final`.
-   Confira os caminhos de importação e os `__init__.py` necessários.

### Relatório não aparece

Abra as ferramentas do navegador com `F12`: - **Console:** mensagens e
erros JavaScript. - **Network/Rede:** respostas de `/messages`, `/audio`
e `/interpretations`. Confira se a resposta de interpretação possui os
campos esperados pela função que renderiza o relatório.
------------------------------------------------------------------------