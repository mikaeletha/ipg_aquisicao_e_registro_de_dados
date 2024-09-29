import serial
import csv
from datetime import datetime

porta_serial = 'COM3'  # Substitua pelo nome da porta serial do seu dispositivo
baud_rate = 9600
timeout = 1

nome_arquivo = 'dados_luz_duplicado.csv'

ser = serial.Serial(porta_serial, baud_rate, timeout=timeout)

with open(nome_arquivo, 'w', newline='') as csvfile:
    fieldnames = ['Index', 'DataHora', 'Luz (lx)', 'Observacao']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

    writer.writeheader()

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
