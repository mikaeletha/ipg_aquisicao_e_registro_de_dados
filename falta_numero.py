import serial
import csv
from datetime import datetime

porta_serial = 'COM3'  # Substitua pelo nome da porta serial do seu dispositivo
baud_rate = 9600
timeout = 1

nome_arquivo = 'dados_luz.csv'

ser = serial.Serial(porta_serial, baud_rate, timeout=timeout)

with open(nome_arquivo, 'w', newline='') as csvfile:
    fieldnames = ['Index', 'DataHora', 'Luz (lx)', 'Observacao']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

    writer.writeheader()

    try:
        lx = []
        index = 0

        while True:
            linha = ser.readline().decode('utf-8').strip()

            if linha:
                luz = str(linha).replace('sensor =', '')
                luz = float(luz)
                data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                observacao = ""
                lx.append(luz)

                if index % 3 == 0 and index != 0:
                    luz_1 = lx[-2]
                    luz_2 = lx[-3]
                    luz = (luz_1 + luz_2) / 2
                    observacao = f"Esse valor e a media de {luz_1} e {luz_2}"

                dados = {
                    'Index': index,
                    'DataHora': data_hora,
                    'Luz (lx)': str(luz).replace('.', ','),
                    'Observacao': observacao
                }

                print(f"Index: {index}, Data: {data_hora}, Luz: {
                      luz} lx, Obeservacao: {observacao}")
                writer.writerow(dados)
                index += 1

    except KeyboardInterrupt:
        print("Interrupção manual pelo usuário.")
    finally:
        ser.close()
        print("Conexão serial fechada.")
