import mysql.connector
from mysql.connector import Error


def test_connection():
    try:
        # Conexão com o banco de dados MySQL
        conn = mysql.connector.connect(
            host='localhost',
            user='ambienteUser',
            password='ambienteUser',
            database='ambiente'
        )

        if conn.is_connected():
            print("Conexão com o banco de dados bem-sucedida!")
        else:
            print("Falha na conexão com o banco de dados.")

    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
    finally:
        if conn.is_connected():
            conn.close()
            print("Conexão com o banco de dados encerrada.")


# Chama a função para testar a conexão
test_connection()


# python test_connection.py
