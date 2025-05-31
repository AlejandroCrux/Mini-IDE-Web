def analizar_lexico_con_diccionario(code):
    palabras_clave = {"if", "else", "while", "for", "return"}
    simbolos_validos = {"(": "P_IZQ", ")": "P_DER", 
                        "{": "LLAVE_I", "}": "LLAVE_D",
                        "+": "SUMA", "-": "RESTA", 
                        "*": "MULT", "/": "DIV", "=": "ASIGNACION"}
    simbolos_error = {";": "P_COMA_NO_PERMT", 
                      ":": "DOS_P_NO_PERMT"}

    tokens = []
    token = ""
    i = 0
    en_comentario = False

    def agregar_token(t):
        if t in palabras_clave:
            tokens.append({"tipo": "PALABRA_CLAVE", "valor": t})
        elif t in simbolos_validos:
            tokens.append({"tipo": simbolos_validos[t], "valor": t})
        elif t in simbolos_error:
            tokens.append({"tipo": "ERROR", "valor": f"Símbolo no permitido '{t}'"})
        elif t.isdigit():
            tokens.append({"tipo": "NUMERO", "valor": t})
        elif t.isidentifier():
            tokens.append({"tipo": "IDENTIFICADOR", "valor": t})
        else:
            tokens.append({"tipo": "DESCONOCIDO", "valor": t})

    while i < len(code):
        char = code[i]
        
        # Manejo de comentarios
        if char == '#':
            if token:
                agregar_token(token)
                token = ""
            # Ignorar el resto de la línea
            while i < len(code) and code[i] != '\n':
                i += 1
            continue
            
        if char.isspace():
            if token:
                agregar_token(token)
                token = ""
        elif char in simbolos_validos or char in simbolos_error:
            if token:
                agregar_token(token)
                token = ""
            agregar_token(char)
        else:
            token += char
        i += 1

    if token:
        agregar_token(token)

    return tokens
