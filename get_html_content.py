import urllib.request
import urllib.error
import urllib.parse

def get_html_content(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'UserAgent/1.0'})
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
            return html_content
    except urllib.error.HTTPError as e:
        print(f"Erro ao obter conteúdo HTML: Código de status {e.code}")
        print(f"Erro ao obter conteúdo HTML: Código de status {url}")
    except urllib.error.URLError as e:
        print(f"Erro de URL: {e.reason}")
    except Exception as e:
        print(f"Erro: {e}")