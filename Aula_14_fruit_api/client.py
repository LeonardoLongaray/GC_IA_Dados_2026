
import requests
from flask import Flask, jsonify
from translate import Translator

base_url = 'https://www.fruityvice.com/api/fruit'

def info_fruta(nome_fruta):
    tradutor = Translator(to_lang='en')
    nome_fruta = tradutor.translate(nome_fruta)

    response = requests.get(f'{base_url}/{nome_fruta}')

    if response.status_code == 200:
        return response.json()
    else:
        return None

fruta = input("Qual fruta você quer consultar? ")
resultado = info_fruta(fruta)

print(resultado)

