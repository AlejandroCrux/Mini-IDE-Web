def analizar_sintactico(code):
    lineas = code.strip().split('\n')
    errores = []
    analisis = []

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
                "fin_codigo": posicion_comentario if posicion_comentario != -1 else len(linea_original)
            })
            continue
        if ":" in linea:
            errores.append({
                "linea": i,
                "mensaje": "Este caracter no es válido ':'",
                "fin_codigo": posicion_comentario if posicion_comentario != -1 else len(linea_original)
            })
            continue

        if any(linea.startswith(clave) for clave in palabras_clave):
            errores.append({
                "linea": i,
                "mensaje": f"El uso de esta palabra reservada no es válido: {linea.split()[0]}",
                "fin_codigo": posicion_comentario if posicion_comentario != -1 else len(linea_original)
            })
            continue

        if "=" in linea:
            partes = linea.split("=")
            if len(partes) != 2:
                errores.append({
                    "linea": i,
                    "mensaje": "Asignación no válida: solo puede tener una sola '='",
                    "fin_codigo": posicion_comentario if posicion_comentario != -1 else len(linea_original)
                })
                continue
            izquierda = partes[0].strip()
            derecha = partes[1].strip()
            
            if not izquierda.isidentifier():
                errores.append({
                    "linea": i,
                    "mensaje": f"El nombre para esta variable no es válido: '{izquierda}'",
                    "fin_codigo": posicion_comentario if posicion_comentario != -1 else len(linea_original)
                })
                continue
            if not derecha:
                errores.append({
                    "linea": i,
                    "mensaje": "El valor para asignar no esta presente",
                    "fin_codigo": posicion_comentario if posicion_comentario != -1 else len(linea_original)
                })
                continue
            
            # Agregar análisis exitoso
            analisis.append(f"✓ Línea {i}: Asignación válida '{izquierda} = {derecha}'")
        else:
            errores.append({
                "linea": i,
                "mensaje": "Línea no válida: falta el operador de asignación '='",
                "fin_codigo": posicion_comentario if posicion_comentario != -1 else len(linea_original)
            })
            continue

    if errores:
        mensaje = f"Se han encontrado errores sintácticos: {len(errores)} línea(s) con problemas."
    else:
        mensaje = "✅ El análisis sintáctico es correcto\n\nDetalles del análisis:\n" + "\n".join(analisis)

    return {
        "resultado": mensaje,
        "errores": errores
    }
