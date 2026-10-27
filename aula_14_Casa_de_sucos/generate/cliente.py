import requests

url = "http://127.0.0.1:5000/sucos"

print("--- Montador de Sucos ---")
nome_suco = input("Qual vai ser o nome do suco? ")

frutas = []
print("Digite os nomes das frutas (digite 'sair' para terminar):")

while True:
    fruta = input("Nome da fruta: ").strip().lower()
    if fruta == 'sair':
        break
    if fruta:
        frutas.append(fruta)

dados_envio = {
    "nome": nome_suco,
    "frutas": frutas
}

resposta = requests.post(url, json=dados_envio)

print("\n--- Resposta do Servidor ---")
print("Status Code:", resposta.status_code)
print(resposta.json())
