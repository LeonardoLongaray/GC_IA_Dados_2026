from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
BASE_URL = "https://www.fruityvice.com/api/fruit"

sucos = []
proximo_id = 1

@app.route('/frutas/<frutas_nomes>', methods=['GET'])
def detalhes_frutas(frutas_nomes): 
    frutas_detalhes = []
    for fruta in frutas_nomes:
        response = requests.get(f"{BASE_URL}/{fruta}")
        if response.status_code == 404:
            return None
        else:
            frutas_detalhes.append(response.json())
        
    return frutas_detalhes

@app.route('/sucos', methods=['GET'])
def listar_sucos():
    return jsonify(sucos)


@app.route('/sucos', methods=['POST'])
def criar_suco():
    global proximo_id
    dados = request.get_json()
    nome_suco = dados.get('nome')
    frutas_nomes = dados.get('frutas')

    frutas_detalhes = detalhes_frutas(frutas_nomes)
    if frutas_detalhes is None:
        return jsonify({"Vish": "Esse não tem."})
    
    suco = {
        "id": proximo_id,
        "nome": nome_suco,
        "frutas": frutas_detalhes,
        "tem gosto de": "suco bom",
        "total_calorias": sum(fruta['nutritions']['calories'] for fruta in frutas_detalhes),
        "total_acucar": sum(fruta['nutritions']['sugar'] for fruta in frutas_detalhes)
        }
    sucos.append(suco)
    proximo_id += 1
    return jsonify(suco)

if __name__ == '__main__':
    app.run(debug=True)