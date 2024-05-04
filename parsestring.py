def parsestring(conteudo, inicio, fim, replace="", ocorrencia=1):
    indice_inicio_busca = 0
    for _ in range(ocorrencia):
        indice_inicio = conteudo.find(inicio, indice_inicio_busca)
        if indice_inicio == -1:
            return ""
        indice_inicio_busca = indice_inicio + len(inicio)
    indice_fim = conteudo.find(fim, indice_inicio_busca)
    if indice_fim == -1:
        return ""
    resultado = conteudo[indice_inicio_busca:indice_fim]
    if replace:
        resultado = resultado.replace(replace, '')
    resultado = resultado.strip()
    
    return resultado