import serial
import csv
from datetime import datetime

porta_serial = 'COM3'  # Substitua pelo nome da porta serial do seu dispositivo
baud_rate = 9600
timeout = 1

ser = serial.Serial(porta_serial, baud_rate, timeout=timeout)

try:
    index = 0
    dados_alterados = []

    while True:
        linha = ser.readline().decode('utf-8').strip()

        if linha:
            # Extrai o valor da luz da string que tem o formato "i: 220 | Luz: 53.33"
            if 'Luz:' in linha:
                try:
                    # Pega apenas a parte com o valor da luz
                    luz = linha.split('| Luz:')[1].strip()
                    luz = float(luz)
                except (IndexError, ValueError):
                    print(f"Erro ao processar a linha: {linha}")
                    continue

                data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                observacao = ""

                dados = {
                    'Index': index,
                    'DataHora': data_hora,
                    'Luz (lx)': str(luz).replace('.', ','),
                    'Observacao': observacao
                }

                # Se múltiplo de 3, duplicar a linha
                if index % 3 == 0 and index != 0:
                    dados_alterados.append(dados.copy())
                    observacao = "Esse valor foi duplicado"
                    dados['Observacao'] = observacao
                    dados_alterados.append(dados.copy())

                    print(f"Index: {index}, Data: {data_hora}, Luz: {
                          luz} lx, Observação: {observacao}")

                else:
                    dados_alterados.append(dados)

                print(f"Index: {index}, Data: {data_hora}, Luz: {
                      luz} lx, Observação: {observacao}")

                index += 1

except KeyboardInterrupt:
    print("Interrupção manual pelo usuário.")
finally:
    ser.close()
    print("Conexão serial fechada.")

    # Remover duplicados
    dados_filtrados = []
    indices_vistos = set()

    for item in dados_alterados:
        if item['Index'] not in indices_vistos:
            dados_filtrados.append(item)
            indices_vistos.add(item['Index'])

    # Salva no csv os dados tratados
    nome_arquivo = 'dados_luz_duplicado.csv'
    with open(nome_arquivo, 'w', newline='') as csvfile:
        fieldnames = ['Index', 'DataHora', 'Luz (lx)', 'Observacao']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()

        for item in dados_filtrados:
            writer.writerow(item)
