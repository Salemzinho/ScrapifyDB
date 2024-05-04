import mysql.connector # type: ignore
import datetime
import json
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from connect_to_database import connect_to_database

def insert_into_database(listing_data, crawler_id, url):
    try:
        # Conecta ao banco de dados
        connection, cursor = connect_to_database()

        today = datetime.datetime.now()
        today_with_seconds = today.replace(second=0, microsecond=0)
        today = today_with_seconds.isoformat()

        # Insere os dados do imóvel na tabela crawler_teste
        query = """
            INSERT INTO crawler_teste 
            (dado1, dado2, dado3, dado4, dado5, dado6, 
            dado7, dado8, dado9, dado10, url, crawler_id) 
            VALUES 
            (%(dado1)s, %(dado2)s, %(dado3)s, %(dado4)s, %(dado6)s, %(cidade)s,
            %(dado7)s, %(dado8)s, %(dado9)s, %(dado10)s, %(url)s, %(crawler_id)s)
        """

        values = {
            'dado1': listing_data.get('dado1') or None,
            'dado2': listing_data.get('dado2') or None,
            'dado3': listing_data.get('dado3') or None,
            'dado4': listing_data.get('dado4') or None,
            'dado5': listing_data.get('dado5') or None,
            'dado6': listing_data.get('dado6') or None,
            'dado7': listing_data.get('dado7') or None,
            'dado8': listing_data.get('dado8') or None,
            'dado9': listing_data.get('dado9') or None,
            'dado10': listing_data.get('dado10') or None,
            'url': url,
            'crawler_id': crawler_id,
        }

        cursor.execute(query, values)
        connection.commit()
        print("Inserção bem sucedida na tabela crawlers_listings")
    except mysql.connector.Error as err:
        print(f"Erro ao inserir na tabela crawlers_listings: {err}")
    except Exception as e:
        print(f"Erro ao inserir na tabela crawlers_listings: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()