def ejecutar_maquina_turing(code):
    cinta = list(code.strip())
    posicion = 0

    
    if not all(simbolo in {'a', 'b'} for simbolo in cinta):
        return "Resultado: Desconocido (caracteres inválidos)"

    log = []

    while posicion < len(cinta):
        simbolo = cinta[posicion]
        if simbolo == 'a':
            cinta[posicion] = 'X'
            log.append(f"Posición {posicion}: 'a' → 'X'")
        elif simbolo == 'b':
            cinta[posicion] = 'Y'
            log.append(f"Posición {posicion}: 'b' → 'Y'")
        posicion += 1

    resultado_final = ''.join(cinta)
    log.append(f"Cinta final: {resultado_final}")

    if code.strip().endswith('a'):
        log.append("Resultado: Es Humano")
    elif code.strip().endswith('b'):
        log.append("Resultado: Es Robot")
    else:
        log.append("Resultado: Desconocido")

    return '\n'.join(log)