import sys
import os
import re
import mysql.connector
import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from insert_into_database import insert_into_database
from connect_to_database import connect_to_database
from get_html_content import get_html_content
from validate_data import validate_data
from parsestring import parsestring
from minify_html import minify_html
from fix_phone import fix_phone

def extract_listing_data(html_content):
    html_content = minify_html(html_content)
    listing_data = {}
    
    listing_data['origem'] = 'nome_do_site'
    
    # Obtem dados do HTML
    listing_data['dado1'] = parsestring(html_content, '<div>', '</div>')
    listing_data['dado2'] = parsestring(html_content, '<span id="dado2">', '</span>')
    listing_data['dado3'] = parsestring(html_content, '<b class="dado3">', '</b>')

    descricao = parsestring(html_content, '<div class="dado4">', '</div>')
    descricao = re.sub('<.*?>', '', descricao)
    listing_data['dado4'] = descricao[:3900]

    # Obtem número de celular e corrige para o +55
    listing_data['dado5'] = parsestring(html_content, 'telefone[', ']')
    if listing_data['dado5'] == "":
        listing_data['dado5'] = parsestring(descricao, 'telefone:"', '"')
    listing_data['dado5'] = fix_phone(listing_data['dado5'])

    # Obtem apenas números no dado
    listing_data['dado6'] = parsestring(html_content, '<li class="dado6">', '</li>')
    listing_data['dado6'] = re.sub('\D', '', listing_data['dado6'])

    # Obtem Valor de venda, preços e etc
    precovenda = parsestring(html_content, '<dado7>R$ ', '</dado7>')
    if precovenda:
        precovenda = re.sub('[^0-9,.]', '', precovenda)
        precovenda = precovenda.replace(".", "").replace(",", ".")
    listing_data['dado7'] = precovenda

    # Obtem imagens de um carousel
    regex = r'<img src="([^"]+)" srcset="'
    matches = re.findall(regex, html_content)
    fotos = matches[:5]
    listing_data['dado8'] = fotos
    
    today = datetime.datetime.now()
    today_with_seconds = today.replace(second=0, microsecond=0)
    today = today_with_seconds.isoformat()
    
    # Obtem a data atual
    listing_data['dado9'] = today
    
    return listing_data

def main():
    try:
        connection, cursor = connect_to_database()

        query = "SELECT id, url FROM crawler_urls WHERE origem = 'nome_do_site' AND concluido = 0;"
        cursor.execute(query)
        urls = cursor.fetchall()

        for crawler_id, url in urls:
            html_content = get_html_content(url)
            if html_content:
                listing_data = extract_listing_data(html_content)
                if listing_data:
                    listing_data = validate_data(listing_data)
                    insert_into_database(listing_data, crawler_id, url)
                    
                    concluido_query = "UPDATE crawler_urls SET concluido = 1 WHERE id = %s;"
                    cursor.execute(concluido_query, (crawler_id,))
                    connection.commit()
    except mysql.connector.Error as err:
        print(f"Erro durante a execução do MySQL: {err}")
    except Exception as e:
        print(f"Erro durante a execução: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    main()