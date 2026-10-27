import requests

url = "http://127.0.0.1:5000/sucos"

print("--- VAMOS FAZER OS MELHORES SUCOS DO MUNDO ---")
nome_suco = input("Qual o nome do MELHOR SUCO DO MUNDO? ")

frutas = []
print("Quais os nomes das MELHORES FRUTAS PARA O MELHOR SUCO DO MUNDO? (digite 'sair' quando terminar de escolher):")

while True:
    fruta = input("Nome da fruta: ").strip().lower()
    if fruta == 'sair':
        break
    elif fruta:
        frutas.append(fruta)

dados_envio = {
    "nome": nome_suco,
    "frutas": frutas
}

resposta = requests.post(url, json=dados_envio)

print("\n--- Resposta do Servidor ---")
print("Status Code:", resposta.status_code)
print(resposta.json())
