import os
import json

PATH = os.path.abspath(os.path.dirname(__file__))
nome_arquivo = 'dados_IQA_regiao_metrop.json'
caminho = os.path.join(PATH, nome_arquivo)

with open(caminho, 'r') as file:
    data = json.load(file)
