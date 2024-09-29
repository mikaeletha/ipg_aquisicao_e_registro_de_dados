import serial
import csv
from datetime import datetime

porta_serial = 'COM3'  # Substitua pelo nome da porta serial do seu dispositivo
baud_rate = 9600
timeout = 1

nome_arquivo = 'dados_luz.csv'

ser = serial.Serial(porta_serial, baud_rate, timeout=timeout)

with open(nome_arquivo, 'w', newline='') as csvfile:
    fieldnames = ['DataHora', 'Luz (lx)']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

    writer.writeheader()

    try:
        index = 0

        while True:
            linha = ser.readline().decode('utf-8').strip()

            if linha:
                luz = str(linha).replace('sensor =', '')
                luz = float(luz)
                data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                if index % 3 != 0 or index == 0:
                    dados = {
                        'DataHora': data_hora,
                        'Luz (lx)': str(luz).replace('.', ',')
                    }
                    print(f"Index: {index}, Data: {data_hora}, Luz: {luz} lx")
                    writer.writerow(dados)

                index = index + 1

    except KeyboardInterrupt:
        print("Interrupção manual pelo usuário.")
    finally:
        ser.close()
        print("Conexão serial fechada.")
