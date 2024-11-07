from random import choice, randint
import json
import os
from typing import List, Dict

PATH = os.path.abspath(os.path.dirname(__file__))
nome_arquivo = 'dados_IQA_regiao_metrop.json'
caminho = os.path.join(PATH, nome_arquivo)

# ----------------------------- PARTE 1: GERAR JSON --------------------------------------
def escrever_json(valores_iniciais: Dict[str, float]) -> None:
    # dict comprehension para criar um json inicial já com valores iniciais
    # data = {chave: [valor] for chave, valor in valores_iniciais.items()}

    # criando o json inicial com context manager 
    with open(caminho, 'w') as arq:
        json.dump(valores_iniciais, arq, ensure_ascii=False, indent=2)

# ----------------------------- PARTE 2: GERAR VALORES --------------------------------------
def gerar_valores_subsequentes(ultimo_valor_gerado: float) -> float:
    '''
        Gera um novo valor subsequente com base em uma variação percentual aleatória 
        do último valor gerado.

        O novo valor é calculado aplicando um desvio percentual aleatório (entre 0% e 50%) 
        ao valor passado, podendo ser positivo ou negativo. Caso o resultado seja negativo,
        retorna 0 para garantir que o valor final nunca seja inferior a 0.

    params::
        ultimo_valor_gerado (float): O último valor gerado, usado como base para calcular
        o novo valor.

    returns::
        float: O novo valor gerado, arredondado para duas casas decimais. Se o valor for 
        menor que 0, retorna 0.
    '''

    std = randint(0, 50)  # desvio em %
    operacao = choice(['+', '-'])
    
    match operacao:
        case '+':
            resultado = ultimo_valor_gerado + (ultimo_valor_gerado * std) / 100
        case '-':
            resultado = ultimo_valor_gerado - (ultimo_valor_gerado * std) / 100
    
    resultado = round(resultado, 2)

    # fiz isso pra garantir que nao seja menor que 0, caso for negativo, ele fica fixo em 0
    return resultado if resultado > 0 else 0

def gerar_valores_json(qtd_valores: int, lista_valores: List[str]) -> float:
    '''
        A função percorre uma lista de itens, abre um arquivo JSON correspondente, lê os dados,
        gera novos valores com base no último valor registrado em cada item, e insere esses 
        valores no arquivo. O processo é repetido até que a quantidade desejada de novos
        valores seja gerada para cada item.

        params::
            qtd_valores (int): A quantidade de valores que será gerada para cada item.
            lista_valores (List[str]): Uma lista contendo os nomes das chaves cujos valores
            serão atualizados no arquivo JSON.
        
        returns::
            float: Retorna o novo valor subsequente gerado para cada item,
            arredondado para duas casas decimais.
    '''

    for _ in range(qtd_valores):
        for item in lista_valores:
            with open(caminho, 'r+') as arq:
                data = json.load(arq)
                novo_valor = gerar_valores_subsequentes(data[item][-1])
                data[item].append(novo_valor)

                arq.seek(0) 
                json.dump(data, arq, ensure_ascii=False, indent=2)
                arq.truncate()

    print('Arquivo json gerado com sucesso!')

if __name__ == '__main__':
    # adicionar poluentes da lista, juntamente com o range num dict para gerar o json inicial
    valores_iniciais = {}
    
    # para adicionar uma margem ao final do intervalo
    offset = 20
    while True:
        poluente = input('Qual poluente? (Pressione enter sem nada preenchido para sair) ').upper()
        if not poluente:
            break
        print('Escreva o range dessa forma: valor1 valor2')
        
        intervalo_inicio, intervalo_fim = map(int, input('Qual intervalo da faixa de concentração para o calculo de IQA? ').split())
        valores_iniciais[poluente] = [randint(intervalo_inicio , intervalo_fim + offset)]
        os.system('cls')
        print(f'{poluente}: [{intervalo_inicio}, {intervalo_fim}] adicionado com sucesso!', end='\n\n')

    escrever_json(valores_iniciais)

    # corresponde a quantas medidas de cada componente você precisa
    while True:
        try:
           qtd_valores = input('Agora me diga a quantidade de valores que você deseja ter para cada poluente: ')
           qtd_valores = int(qtd_valores) - 1
           break
        except ValueError:
            print('Digite um numero, por favor!\n')
            continue

    print(f'\nCerto! Agora abra o arquivo Json na raiz do seu codigo de nome "{nome_arquivo}" e veja a magica acontecer!', end='\n\n')
    lista_valores = valores_iniciais.keys()
    gerar_valores_json(qtd_valores, lista_valores)