import sys
import os
import re
import urllib.request
import urllib.error

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from connect_to_database import connect_to_database

def get_html_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Referer': url, 
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
            return html_content
    except urllib.error.HTTPError as e:
        print(f"Erro ao obter conteúdo HTML: Código de status {e.code}")
    except urllib.error.URLError as e:
        print(f"Erro de URL: {e.reason}")
    except Exception as e:
        print(f"Erro: {e}")

def extract_links(html_content):
    links = []
    # padrão das urls que serão capturadas, exemplo: <a href=""
    pattern = r'<a\s+(?:[^>]*?\s+)?href=(["\'])(.*?)\1'
    matches = re.findall(pattern, html_content)
    for match in matches:
        # filtro das urls que serão capturadas, exemplo /teste
        if '/teste' in match[1]:
            links.append(match[1])
    return links

def url_exists_in_database(url, cursor):
    query = "SELECT COUNT(*) FROM crawler_urls WHERE url = %s and origem = 'nome_do_site'"
    cursor.execute(query, (url,))
    result = cursor.fetchone()[0]
    return result > 0

def insert_into_database(links):
    try:
        connection, cursor = connect_to_database()
        for link in links:
            if not url_exists_in_database(link, cursor):
                query = "INSERT INTO crawler_urls (url, result_text, origem) VALUES (%s, %s, %s)"
                values = (link, link, 'nome_do_site')
                cursor.execute(query, values)
        connection.commit()
        print("Inserção bem sucedida na tabela crawlers")
    except Exception as e:
        print(f"Erro ao inserir na tabela crawlers: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def main():
    # url base, exemplo: https://www.teste.com.br
    base_url = "https://www.teste.com.br"
    categorias = ["marketing", "compras"]
    all_links = []
    for categoria in categorias:
        for i in range(1, 2): # iterando sobre 1 páginas em cada categoria
            url = f"{base_url}/{categoria}/"
            html_content = get_html_content(url)
            if html_content:
                links = extract_links(html_content)
                all_links.extend(links)
    print("Todas as URLs coletadas:")
    for link in all_links:
        print(link)
    
    insert_into_database(all_links)

if __name__ == "__main__":
    main()