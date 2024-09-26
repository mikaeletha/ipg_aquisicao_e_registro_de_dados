import serial
import csv
from datetime import datetime

porta_serial = 'COM3'  # Substitua pelo nome da porta serial do seu dispositivo
baud_rate = 9600
timeout = 1

nome_arquivo = 'dados_tensao.csv'

ser = serial.Serial(porta_serial, baud_rate, timeout=timeout)

with open(nome_arquivo, 'w', newline='') as csvfile:
    fieldnames = ['DataHora', 'Tensao (V)']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

    writer.writeheader()

    try:
        while True:
            linha = ser.readline().decode('utf-8').strip()

            if linha:
                try:
                    # Verifica se a string recebida contém apenas números (inclui ponto decimal)
                    if linha.replace('.', '', 1).isdigit():
                        # Converte a linha para float
                        leitura_bruta = float(linha)
                        # Converte leitura ADC para tensão
                        tensao = (leitura_bruta / 1023.0) * 3.0
                        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                        dados = {
                            'DataHora': data_hora,
                            'Tensao (V)': str(tensao).replace('.', ',')
                        }

                        print(f"Data: {data_hora}, Tensão: {tensao} V")

                        writer.writerow(dados)
                    else:
                        print(f"Valor não numérico recebido: {linha}")
                except ValueError:
                    print(f"Erro ao converter valor: {linha}")

    except KeyboardInterrupt:
        print("Interrupção manual pelo usuário.")
    finally:
        ser.close()
        print("Conexão serial fechada.")
