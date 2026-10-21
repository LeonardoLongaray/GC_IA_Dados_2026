import requests

BASE_URL = 'http://localhost:5000'

def obter_tarefas():
    resposta = requests.get(f'{BASE_URL}/tarefas')
    return resposta.json()

def criar_tarefa(descricao):
    resposta = requests.post(f'{BASE_URL}/tarefas', json={'descricao': descricao})
    return resposta.json()

def atualizar_tarefa(tarefa_id, **campos):
    resposta = requests.put(f'{BASE_URL}/tarefas/{tarefa_id}', json=campos)
    return resposta.json()

def excluir_tarefa(tarefa_id):
    resposta = requests.delete(f'{BASE_URL}/tarefas/{tarefa_id}')
    return resposta.json()

def executar_exemplos():
    print('Lista inicial:', obter_tarefas())
    print('Criando tarefa:', criar_tarefa('Estudar Python'))
    print('Criando outra:', criar_tarefa('Escrever artigo'))
    print('Marcando a primeira como concluída:',
          atualizar_tarefa(1, concluida=True))
    print('Excluindo a segunda:', excluir_tarefa(2))
    print('Lista final:', obter_tarefas())

if __name__ == '__main__':
    executar_exemplos()