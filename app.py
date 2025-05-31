from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

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
    errores = []
    linea_actual = 1
    columna_actual = 0

    def agregar_token(t, linea, columna):
        if t in palabras_clave:
            tokens.append({"tipo": "PALABRA_CLAVE", "valor": t, "linea": linea, "columna": columna})
        elif t in simbolos_validos:
            tokens.append({"tipo": simbolos_validos[t], "valor": t, "linea": linea, "columna": columna})
        elif t in simbolos_error:
            tokens.append({"tipo": "ERROR", "valor": t, "linea": linea, "columna": columna})
            errores.append({"mensaje": f"Símbolo no permitido '{t}'", "linea": linea, "columna": columna})
        elif t.isdigit():
            tokens.append({"tipo": "NUMERO", "valor": t, "linea": linea, "columna": columna})
        elif t.isidentifier():
            tokens.append({"tipo": "IDENTIFICADOR", "valor": t, "linea": linea, "columna": columna})
        else:
            tokens.append({"tipo": "DESCONOCIDO", "valor": t, "linea": linea, "columna": columna})
            errores.append({"mensaje": f"Token desconocido '{t}'", "linea": linea, "columna": columna})

    while i < len(code):
        char = code[i]
        if char == '\n':
            if token:
                agregar_token(token, linea_actual, columna_actual - len(token))
                token = ""
            linea_actual += 1
            columna_actual = 0
        else:
            columna_actual += 1
            if char.isspace():
                if token:
                    agregar_token(token, linea_actual, columna_actual - len(token))
                    token = ""
            elif char in simbolos_validos or char in simbolos_error:
                if token:
                    agregar_token(token, linea_actual, columna_actual - len(token))
                    token = ""
                agregar_token(char, linea_actual, columna_actual)
            else:
                token += char
        i += 1

    if token:
        agregar_token(token, linea_actual, columna_actual - len(token) + 1)

    return {"tokens": tokens, "errores": errores}

def analizar_sintactico(code):
    lineas = code.strip().split('\n')
    errores = []

    palabras_clave = ("if", "while", "for", "def", "else", "elif")

    for i, linea in enumerate(lineas, start=1):
        posicion_comentario = linea.find('#')
        linea_original = linea
        
        if posicion_comentario != -1:
            linea = linea[:posicion_comentario]
        
        linea = linea.strip()
        if not linea: 
            continue

        if ";" in linea:
            errores.append({
                "linea": i,
                "mensaje": "Este caracter no es válido ';'",
                "columna": linea.find(';')
            })
            continue
        if ":" in linea:
            errores.append({
                "linea": i,
                "mensaje": "Este caracter no es válido ':'",
                "columna": linea.find(':')
            })
            continue

        if any(linea.startswith(clave) for clave in palabras_clave):
            errores.append({
                "linea": i,
                "mensaje": f"El uso de esta palabra reservada no es válido: {linea.split()[0]}",
                "columna": 0
            })
            continue

        if "=" in linea:
            partes = linea.split("=")
            if len(partes) != 2:
                errores.append({
                    "linea": i,
                    "mensaje": "Asignación no válida: solo puede tener una sola '='",
                    "columna": linea.find('=', linea.find('=') + 1)
                })
                continue
            izquierda = partes[0].strip()
            derecha = partes[1].strip()
            if not izquierda.isidentifier():
                errores.append({
                    "linea": i,
                    "mensaje": f"El nombre para esta variable no es válido: '{izquierda}'",
                    "columna": 0
                })
                continue
            if not derecha:
                errores.append({
                    "linea": i,
                    "mensaje": "El valor para asignar no esta presente",
                    "columna": len(linea)
                })
                continue
        else:
            errores.append({
                "linea": i,
                "mensaje": "Línea no válida: falta el operador de asignación '='",
                "columna": 0
            })
            continue

    return {
        "errores": errores,
        "resultado": "El análisis sintáctico es correcto" if not errores else f"Se han encontrado errores sintácticos: {len(errores)} línea(s) con problemas."
    }

def ejecutar_maquina_turing(code):
    cinta = list(code.strip())
    posicion = 0
    historial = []

    if not all(simbolo in {'a', 'b'} for simbolo in cinta):
        return {
            "error": True,
            "mensaje": "Error: Solo se permiten los caracteres 'a' y 'b'",
            "historial": [],
            "resultado": "Desconocido"
        }

    while posicion < len(cinta):
        estado_actual = {
            "cinta": ''.join(cinta),
            "posicion": posicion,
            "simbolo_actual": cinta[posicion]
        }
        
        if cinta[posicion] == 'a':
            cinta[posicion] = 'X'
            estado_actual["nuevo_simbolo"] = 'X'
        elif cinta[posicion] == 'b':
            cinta[posicion] = 'Y'
            estado_actual["nuevo_simbolo"] = 'Y'
            
        historial.append(estado_actual)
        posicion += 1

    resultado_final = ''.join(cinta)
    tipo = "Es Humano" if code.strip().endswith('a') else "Es Robot" if code.strip().endswith('b') else "Desconocido"

    return {
        "error": False,
        "historial": historial,
        "resultado_final": resultado_final,
        "tipo": tipo
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analizar_lexico', methods=['POST'])
def analizar_lexico():
    codigo = request.json.get('codigo', '')
    return jsonify(analizar_lexico_con_diccionario(codigo))

@app.route('/analizar_sintactico', methods=['POST'])
def analizar_sintactico_route():
    codigo = request.json.get('codigo', '')
    return jsonify(analizar_sintactico(codigo))

@app.route('/ejecutar_turing', methods=['POST'])
def ejecutar_turing():
    entrada = request.json.get('entrada', '')
    return jsonify(ejecutar_maquina_turing(entrada))

if __name__ == '__main__':
    app.run(debug=True)
