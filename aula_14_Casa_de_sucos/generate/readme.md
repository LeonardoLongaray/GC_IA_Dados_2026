Projeto desenvolvido para praticar a criação e o consumo de APIs utilizando Python, Flask e Requests.

A aplicação permite cadastrar sucos com diferentes frutas, consultar os sucos cadastrados e atualizar suas frutas e informações nutricionais.

## 📋 Bibliotecas utilizadas

- **Python:** linguagem de programação.
- **Flask:** criação da API.
- **Requests:** realização de requisições HTTP para consultar informações das frutas.
- **Postman:** ferramenta para testar as rotas da API.

## 📁 Estrutura do projeto

```text
aula_14_casa_de_sucos/generate
├── app.py
├── cliente.py
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Pré-requisitos

Descrito em requirements.txt

## 🐍 Criar o ambiente virtual

Crie um ambiente virtual para instalar as dependências isoladamente:

```cmd
python -m venv venv
```

Ative o ambiente virtual no Windows CMD:

```cmd
venv\Scripts\activate
```

Após a ativação, o terminal deverá mostrar `(venv)` antes do caminho ou do cursor.

## 📦 Instalar as dependências

Com o ambiente virtual ativado, execute:

```cmd
python -m pip install -r requirements.txt
```

Esse comando instala as bibliotecas necessárias ao projeto.


## 🚀 Iniciar a API (`app.py`)

Abra um terminal do CMD na pasta do projeto, ative o ambiente virtual e execute:

```cmd
python app.py
```

Se tudo estiver correto, o Flask deverá informar que o servidor está disponível em:

`http://127.0.0.1:5000`

**Importante:** mantenha esse terminal aberto enquanto estiver utilizando a API. Se ele for fechado, o servidor será encerrado.

## 🧃 Executar o cliente (`cliente.py`)

Com a API já iniciada, abra um **segundo terminal** na pasta do projeto.

Ative o ambiente virtual nesse novo terminal:

```cmd
venv\Scripts\activate
```

Execute o cliente:

```cmd
python cliente.py
```

Siga as perguntas apresentadas pelo programa para informar o nome do suco e as frutas desejadas.

O cliente realiza requisições HTTP para a API local, que processa os dados e consulta as informações nutricionais das frutas.


## 🧪 Testar a API com o Postman

Com o servidor Flask em execução, abra o Postman e utilize o endereço-base:

`http://127.0.0.1:5000`

### Consultar os sucos cadastrados

- **Método:** `GET`
- **URL:** `http://127.0.0.1:5000/sucos`

Clique em **Send** para visualizar os sucos cadastrados.

### Cadastrar um suco

- **Método:** `POST`
- **URL:** `http://127.0.0.1:5000/sucos`
- **Body:** `raw` → `JSON`

Exemplo de corpo da requisição:

```json
{
    "nome": "Suco Tropical",
    "frutas": ["banana", "apple"]
}
```

Os campos devem corresponder aos esperados pela implementação atual da rota `POST`.

### Atualizar as frutas de um suco

- **Método:** `PUT`
- **URL:** `http://127.0.0.1:5000/sucos/1`
- **Body:** `raw` → `JSON`

Exemplo:

```json
{
    "frutas": ["banana", "apple", "pineapple"]
}
```

O número `1` na URL representa o ID do suco que será atualizado. Utilize um ID existente na lista.

A API consulta os dados das frutas, atualiza as informações nutricionais e retorna o suco atualizado.
