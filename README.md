# Mini IDE Web

## Información del Proyecto
- **Alumno:** Alejandro Cruz López
- **Profesor:** Kevin David Molina Gomez
- **Materia:** Lenguajes y Automatas I

## Instrucciones de Ejecución

1. Asegúrate de tener Python 3.x instalado
2. Instala las dependencias necesarias:
   ```bash
   pip install flask
   ```
3. Ejecuta el servidor:
   ```bash
   python app.py
   ```
4. Abre tu navegador y visita: `http://localhost:5000`

## Lenguaje Personalizado

### Tokens
- **IDENTIFICADOR**: Nombres de variables (ej: x, nombre, edad)
- **NUMERO**: Valores numéricos (ej: 42, 100)
- **PALABRA_CLAVE**: Palabras reservadas (if, else, while, for, return)
- **OPERADORES**: 
  - SUMA (+)
  - RESTA (-)
  - MULT (*)
  - DIV (/)
  - ASIGNACION (=)
- **SÍMBOLOS**:
  - P_IZQ: Paréntesis izquierdo (
  - P_DER: Paréntesis derecho )
  - LLAVE_I: Llave izquierda {
  - LLAVE_D: Llave derecha }

### Gramática
El lenguaje acepta:
- Asignaciones simples: `variable = valor`
- Operaciones aritméticas básicas: `resultado = x + y`
- No se permiten estructuras de control (if, while, for)
- No se permiten símbolos especiales como `;` o `:`

### Errores Detectados
1. **Léxicos:**
   - Símbolos no permitidos (;, :)
   - Caracteres desconocidos
   - Tokens inválidos

2. **Sintácticos:**
   - Uso de palabras reservadas
   - Asignaciones inválidas
   - Falta de operador de asignación
   - Nombres de variables inválidos

## Ejemplos

### Código Válido
```python
# Variables y operaciones básicas
x = 42
y = x + 10
resultado = x * y

# Asignaciones válidas
nombre = "Juan"
edad = 25
suma = a + b
```

### Código Inválido
```python
# Estructuras de control (no permitidas)
if x > 0:
while true;
for i in range

# Errores comunes
variable;
resultado = 
```

### Máquina de Turing
La máquina de Turing implementada acepta secuencias de 'a' y 'b':
- Secuencia Humano: `aabaa`
- Secuencia Robot: `aabab`

## Características Adicionales
- Editor de código con resaltado de sintaxis
- Modo oscuro/claro
- Botón de apoyo emocional con GIF animado
- Visualización detallada de tokens y errores
- Ejemplos predefinidos
- Interfaz responsiva 