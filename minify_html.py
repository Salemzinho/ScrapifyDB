import re

def minify_html(html):
    html = re.sub(r"<!--(.*?)-->", "", html)
    html = re.sub(r">\s+<", "><", html)
    html = re.sub(r"\n+", "", html)
    html = re.sub(r"\s{2,}", " ", html)
    return html.strip()