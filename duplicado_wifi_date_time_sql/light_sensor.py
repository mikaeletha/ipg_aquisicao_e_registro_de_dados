import serial
import mysql.connector

# Conexão com o banco de dados MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='ambienteUser',
    password='ambienteUser',
    database='ambiente'
)

cursor = conn.cursor()

porta_serial = 'COM3'  # Substitua pelo nome da porta serial do seu dispositivo
baud_rate = 9600
timeout = 1

ser = serial.Serial(porta_serial, baud_rate, timeout=timeout)

# Variáveis para armazenar a última linha recebida
ultima_index = None
ultima_luz = None
ultima_data_hora = None

try:
    while True:
        linha = ser.readline().decode('utf-8').strip()

        if linha:
            partes = linha.split(';')

            index = int(partes[0].strip())
            luz = float(partes[1].strip())
            data_hora = partes[2].strip()

            # Verifica se a linha atual é diferente da última linha recebida
            if (index != ultima_index) or (luz != ultima_luz) or (data_hora != ultima_data_hora):
                print(f"Índice: {index}, Luz: {
                      luz} lx, Data/Hora: {data_hora}")

                # Salva os dados no banco de dados
                cursor.execute('''
                INSERT INTO dados (id_dados, valor, data_hora)
                VALUES (%s, %s, %s)
                ''', (index, luz, data_hora))
                conn.commit()  # Confirma a transação

                # Atualiza a última linha recebida
                ultima_index = index
                ultima_luz = luz
                ultima_data_hora = data_hora
            else:
                print("Linha duplicada ignorada.")

except KeyboardInterrupt:
    print("Interrupção manual pelo usuário.")

finally:
    ser.close()
    cursor.close()  # Fecha o cursor
    conn.close()  # Fecha a conexão com o banco de dados
    print("Conexão serial fechada e conexão com o banco de dados encerrada.")
