import serial
import csv
from datetime import datetime

porta_serial = 'COM3'  # Substitua pelo nome da porta serial do seu dispositivo
baud_rate = 9600
timeout = 1

ser = serial.Serial(porta_serial, baud_rate, timeout=timeout)

try:
    index = 0
    observacao = ""
    dados_duplicados = []

    while True:
        linha = ser.readline().decode('utf-8').strip()

        if linha:
            luz = str(linha).replace('sensor =', '').strip()
            luz = float(luz)
            data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            dados = {
                'Index': index,
                'DataHora': data_hora,
                'Luz (lx)': str(luz).replace('.', ','),
                'Observacao': observacao
            }

            # Se múltiplo de 3, duplicar a linha
            if index % 3 == 0 and index != 0:
                dados_duplicados.append(dados.copy())
                dados['Observacao'] = "Esse valor foi duplicado"
                dados_duplicados.append(dados.copy())

            else:
                dados_duplicados.append(dados)

            print(f"Index: {index}, Data: {data_hora}, Luz: {
                luz} lx")

            index += 1

except KeyboardInterrupt:
    print("Interrupção manual pelo usuário.")
finally:
    ser.close()
    print("Conexão serial fechada.")

    print("\nDados duplicados:")
    for item in dados_duplicados:
        print(f"Index: {item['Index']}, Data: {item['DataHora']}, Luz: {
            item['Luz (lx)']}, Observação: {item['Observacao']}")

    # Remover duplicados
    dados_filtrados = []
    indices_vistos = set()

    for item in dados_duplicados:
        if item['Index'] not in indices_vistos:
            dados_filtrados.append(item)
            indices_vistos.add(item['Index'])

    # Exibe os dados após remoção dos duplicados
    # print("\nDados após remoção de duplicados:")
    # for item in dados_filtrados:
    #     print(f"Index: {item['Index']}, Data: {item['DataHora']}, Luz: {
    #           item['Luz (lx)']}")

    # Salva no csv os dados tratados
    nome_arquivo = 'dados_luz_duplicado.csv'
    with open(nome_arquivo, 'w', newline='') as csvfile:
        fieldnames = ['Index', 'DataHora', 'Luz (lx)', 'Observacao']
        writer = csv.DictWriter(
            csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()

        for item in dados_filtrados:
            writer.writerow(item)
