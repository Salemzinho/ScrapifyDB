import mysql.connector

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="",
            user="",
            password="",
            database=""
        )
        cursor = connection.cursor()
        return connection, cursor
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None, None