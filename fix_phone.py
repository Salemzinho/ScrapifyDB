def fix_phone(numero):
    numero = numero.strip()
    if numero == "":
        return ""

    numero = numero.replace('(', '').replace(')', '').replace(' ', '').replace('-', '').replace('/', '').replace('+', '')
    numero = ''.join(filter(str.isdigit, numero))

    if numero.startswith("0"):
        numero = numero[1:]

    if len(numero) == 9:
        numero = '11' + numero

    if not numero.startswith("55"):
        numero = "55" + numero

    return numero