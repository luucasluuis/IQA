import os
import json

#tentando abrir o arquivo json

PATH = os.path.abspath(os.path.dirname(__file__))
nome_arquivo = 'dados_IQA_regiao_metrop.json'
caminho = os.path.join(PATH, nome_arquivo)


with open(caminho, 'r') as file:
        data = json.load(file)


# classificação do IQA
def classificar_IQA(iqa):
    if 0 <= iqa <= 50:
        return "Qualidade BOA"
    elif 51 <= iqa <= 100:
        return "Qualidade REGULAR"
    elif 101 <= iqa <= 199:
        return "Qualidade INADEQUADA"
    elif 200 <= iqa <= 299:
        return "Qualidade MÁ"
    elif iqa >= 300:
        return "Qualidade PÉSSIMA"
    else:
        return "Valor fora da escala"

#equação para o IQA
    
def calcular_IQA(C, Cf, Ci, If, Ii):
    Ip = ((If - Ii) / (Cf - Ci)) * (C - Ci) + Ii
    return Ip

faixas_concentracao = {
    'SO2': [
         [0, 80],
         [81, 365],
         [366, 800],
         [801, 1600],
         [1600, 0]
    ],
    'CO': [
         [0, 4],
         [4.1, 9],
         [9.1, 15],
         [15.1, 30],
         [30, 0]
    
    ],
    'PM10': [
         [0, 50],
         [51, 150],
         [151, 250],
         [251, 420],
         [420, 0]
    
    ],
    'O3': [
         [0, 80],
         [81, 160],
         [161, 200],
         [201, 800],
         [800, 0]
    
    ],
    'NO2': [
         [0, 100],
         [101, 320],
         [321, 1130],
         [1131, 2260],
         [2260, 0]
    
    ],
}

valores_iqa = [(0, 50), (51, 100), (101, 200), (201, 300), (300, 0)]
print(valores_iqa)
resultados_ip = {}
# parametros_do_ar = {
# }
#constantes e variáveis da equação
for nome, dados in data.items():
        media_valor = sum(dados) / len(dados)
        # parametros_do_ar[nome] = media_valor[]
        indice = 0
        for valores in faixas_concentracao.values():
            while not (valores[indice][0] <= media_valor <= valores[indice][1]):
                indice += 1
                break
            break
        calculo_ip = calcular_IQA(
                                media_valor, \
                                valores_iqa[indice][1],\
                                valores_iqa[indice][0],\
                                valores[indice][1],\
                                valores[indice][0]
                            )

        resultados_ip[nome] = calculo_ip          

print(resultados_ip)

# Ip = (300 - 201 / 1600 - 801) * (1201.85 - 801) + 201
#resultado
# Ip = calcular_IQA(media_valor, Cf, Ci, If, Ii)
# resultados[nome] = Ip


# poluente_dominante = max(resultados, key=resultados.get)

# print(f"Poluente dominante: {poluente_dominante}, Valor IQA: {resultados[poluente_dominante]}")
# for poluente, valor in resultados.items():
#     print(f"{poluente}: {valor} ({classificar_IQA(valor)})")

# fazer um gráfico