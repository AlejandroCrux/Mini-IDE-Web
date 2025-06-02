// Configuración del editor CodeMirror
let editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
    mode: "python",
    theme: "neat",
    lineNumbers: true,
    indentUnit: 4
});

// Variables globales
const themeSwitch = document.getElementById('themeSwitch');
const supportSwitch = document.getElementById('supportSwitch');
const html = document.documentElement;
const emotionalSupport = document.querySelector('.emotional-support');

// Ejemplos predefinidos
const ejemplos = {
    lexico1: `# Variables y operaciones básicas
x = 42
y = x + 10
resultado = x * y`,
    lexico2: `# Estructuras de control (con errores)
if x > 0:
while true;
for i in range`,
    sintactico1: `# Asignaciones válidas
nombre = "Juan"
edad = 25
suma = a + b`,
    sintactico2: `# Errores comunes
if x > 0:
variable;
resultado = `,
    turing1: `aabaa`,
    turing2: `aabab`
};

// Funciones de tema y soporte emocional
function setInitialTheme() {
    const isDarkMode = html.getAttribute('data-bs-theme') === 'dark';
    themeSwitch.checked = isDarkMode;
    editor.setOption('theme', isDarkMode ? 'monokai' : 'neat');
}

// Event Listeners
themeSwitch.addEventListener('change', function() {
    if (this.checked) {
        html.setAttribute('data-bs-theme', 'dark');
        editor.setOption('theme', 'monokai');
    } else {
        html.setAttribute('data-bs-theme', 'light');
        editor.setOption('theme', 'neat');
    }
});

supportSwitch.addEventListener('change', function() {
    emotionalSupport.style.display = this.checked ? 'block' : 'none';
});

// Funciones de manejo de ejemplos
function cargarEjemplo(tipo) {
    const ejemplo = ejemplos[tipo];
    if (tipo.startsWith('turing')) {
        document.getElementById('entrada-turing').value = ejemplo;
        ejecutarTuring();
    } else {
        editor.setValue(ejemplo);
        if (tipo.startsWith('lexico')) {
            analizarLexico();
        } else if (tipo.startsWith('sintactico')) {
            analizarSintactico();
        }
    }
}

// Funciones de limpieza
function limpiarResultados() {
    document.getElementById('resultados').textContent = '';
    limpiarErrores();
}

function limpiarEditor() {
    editor.setValue('');
    limpiarErrores();
    document.getElementById('resultados').textContent = '';
}

function limpiarErrores() {
    editor.getAllMarks().forEach(mark => mark.clear());
    for (let i = 0; i < editor.lineCount(); i++) {
        editor.removeLineClass(i, 'background', 'error-line');
    }
}

function limpiarTuring() {
    document.getElementById('entrada-turing').value = '';
    document.getElementById('resultado-turing').textContent = '';
    document.getElementById('cinta-turing').textContent = '';
    document.getElementById('clasificacion-turing').textContent = '';
}

// Función para marcar errores en el editor
function marcarError(linea, columna, mensaje) {
    const lineIndex = linea - 1;
    
    editor.addLineClass(lineIndex, 'background', 'error-line');
    
    if (columna !== undefined) {
        const lineContent = editor.getLine(lineIndex);
        let endCh = columna + 1;
        
        if (mensaje.includes("no permitido") || mensaje.includes("inválido")) {
            while (endCh < lineContent.length && !lineContent[endCh].match(/\s/)) {
                endCh++;
            }
        }
        
        editor.markText(
            { line: lineIndex, ch: columna },
            { line: lineIndex, ch: endCh },
            { 
                className: 'error-underline',
                title: mensaje
            }
        );
    }
}

// Funciones de análisis y ejecución
async function analizarLexico() {
    limpiarErrores();
    const codigo = editor.getValue().trim();
    
    if (!codigo) {
        document.getElementById('resultados').textContent = "⚠️ El editor de código está vacío.\nPor favor, ingrese código para analizar.";
        return;
    }

    try {
        const response = await fetch('/analizar_lexico', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ codigo })
        });
        const data = await response.json();
        
        let resultado = document.createElement('div');
        
        if (data.tokens.length > 0) {
            resultado.appendChild(document.createTextNode("Tokens encontrados:"));
            
            let tabla = document.createElement('table');
            tabla.className = 'token-table';
            
            let thead = document.createElement('thead');
            let headerRow = document.createElement('tr');
            ['Valor', 'Tipo', 'Línea', 'Columna'].forEach(header => {
                let th = document.createElement('th');
                th.textContent = header;
                headerRow.appendChild(th);
            });
            thead.appendChild(headerRow);
            tabla.appendChild(thead);
            
            let tbody = document.createElement('tbody');
            data.tokens.forEach(token => {
                let row = document.createElement('tr');
                if (token.tipo === "ERROR" || token.tipo === "DESCONOCIDO") {
                    row.className = 'error-row';
                }
                [token.valor, token.tipo, token.linea, token.columna].forEach(cell => {
                    let td = document.createElement('td');
                    td.textContent = cell;
                    row.appendChild(td);
                });
                tbody.appendChild(row);
                
                if (token.tipo === "ERROR" || token.tipo === "DESCONOCIDO") {
                    marcarError(token.linea, token.columna, `Error léxico: ${token.valor}`);
                }
            });
            tabla.appendChild(tbody);
            resultado.appendChild(tabla);
        }

        if (data.errores.length > 0) {
            let errorDiv = document.createElement('div');
            errorDiv.style.marginTop = '20px';
            errorDiv.appendChild(document.createTextNode("Errores encontrados:\n"));
            data.errores.forEach(error => {
                let errorText = document.createTextNode(
                    `Línea ${error.linea}, Columna ${error.columna}: ${error.mensaje}\n`
                );
                errorDiv.appendChild(errorText);
                marcarError(error.linea, error.columna, error.mensaje);
            });
            resultado.appendChild(errorDiv);
        }

        const resultadosDiv = document.getElementById('resultados');
        resultadosDiv.textContent = '';
        resultadosDiv.appendChild(resultado);
    } catch (error) {
        console.error('Error:', error);
    }
}

async function analizarSintactico() {
    limpiarErrores();
    const codigo = editor.getValue().trim();
    
    if (!codigo) {
        document.getElementById('resultados').textContent = "⚠️ El editor de código está vacío.\nPor favor, ingrese código para analizar.";
        return;
    }

    try {
        const response = await fetch('/analizar_sintactico', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ codigo })
        });
        const data = await response.json();
        
        let resultado = data.resultado + "\n\n";
        if (data.errores.length > 0) {
            resultado += "Detalles de los errores:\n";
            data.errores.forEach(error => {
                resultado += `Línea ${error.linea}: ${error.mensaje}\n`;
                marcarError(error.linea, error.columna, error.mensaje);
            });
        }

        document.getElementById('resultados').textContent = resultado;
    } catch (error) {
        console.error('Error:', error);
    }
}

async function ejecutarTuring() {
    const entrada = document.getElementById('entrada-turing').value;
    try {
        const response = await fetch('/ejecutar_turing', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ entrada })
        });
        const data = await response.json();

        if (data.error) {
            document.getElementById('resultado-turing').textContent = data.mensaje;
            document.getElementById('cinta-turing').textContent = '';
            document.getElementById('clasificacion-turing').textContent = '';
            return;
        }

        let resultado = '';
        data.historial.forEach((estado, index) => {
            resultado += `Paso ${index + 1}:\n`;
            resultado += `Cinta: ${estado.cinta}\n`;
            resultado += `Posición: ${estado.posicion}\n`;
            resultado += `Cambio: ${estado.simbolo_actual} → ${estado.nuevo_simbolo}\n\n`;
        });
        resultado += `Resultado: ${data.resultado_final}\n`;

        document.getElementById('clasificacion-turing').textContent = `Clasificación: ${data.tipo}`;
        document.getElementById('resultado-turing').textContent = resultado;
        
        const cintaDiv = document.getElementById('cinta-turing');
        const ultimoEstado = data.historial[data.historial.length - 1];
        cintaDiv.textContent = ultimoEstado ? ultimoEstado.cinta : '';
    } catch (error) {
        console.error('Error:', error);
    }
}

// Inicialización
setInitialTheme(); 