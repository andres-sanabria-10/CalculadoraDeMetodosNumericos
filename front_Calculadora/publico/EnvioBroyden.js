const crearButton = document.getElementById('crear');
const numFilasInput = document.getElementById('num_filas');
const numColumnasInput = document.getElementById('num_columnas');
const matrixContainer = document.getElementById('matrixContainer');
const contenedorGrafico = document.querySelector('.scrollable-container');

// Evento para crear y mostrar el modal con los inputs
crearButton.addEventListener('click', function (event) {
    event.preventDefault();
    // Obtén los valores de filas y columnas
    const numFilas = parseInt(numFilasInput.value);
    const numColumnas = parseInt(numColumnasInput.value);

    // Verifica si son valores válidos y si forman una matriz cuadrada
    if (isNaN(numFilas) || isNaN(numColumnas)) {
        alert('Por favor, ingrese valores numéricos en las filas y columnas.');
        return;
    }

    if (numFilas <= 0 || numColumnas <= 0) {
        alert('Las filas y columnas deben ser mayores que 0.');
        return;
    }

    if (numFilas !== numColumnas) {
        alert('El sistema de ecuaciones debe ser cuadrado.');
        return;
    }

    generarMatriz(numFilas, numColumnas);

});

// Generar la matriz de inputs dinámicamente
function generarMatriz(filas, columnas) {
    contenedorGrafico.innerHTML = ''; // Limpiar contenido previo

    // Crear tabla
    const tabla = document.createElement('table');
    tabla.className = 'matrix-table';

    // Crear encabezado
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');

    // Celda vacía para la esquina superior izquierda
    const cornerCell = document.createElement('th');
    headerRow.appendChild(cornerCell);

    

    // Encabezados X1, X2, etc.
    for (let j = 1; j <= columnas; j++) {
        const th = document.createElement('th');
        th.innerText = `X${j}`;
        headerRow.appendChild(th);
    }

    // Encabezado b
    const thB = document.createElement('th');
    thB.innerText = 'puntos';
    headerRow.appendChild(thB);

    thead.appendChild(headerRow);
    tabla.appendChild(thead);

    // Crear cuerpo de la tabla
    const tbody = document.createElement('tbody');
    for (let i = 0; i < filas; i++) {
        const tr = document.createElement('tr');

        // Número de fila
        const rowLabel = document.createElement('td');
        rowLabel.className = 'matrix-row-label';
        rowLabel.innerText = i + 1;
        tr.appendChild(rowLabel);

        // Inputs para X1, X2, etc. y b
        for (let j = 0; j <= columnas; j++) {
            const td = document.createElement('td');
            const input = document.createElement('input');
            input.type = 'text';
            input.className = 'matrix-input-control matrix-input-size calculator-input'; // Asegúrate de mantener calculator-input
            input.placeholder = j === columnas ? 'puntos' : `X${j + 1}`;
            td.appendChild(input);
            tr.appendChild(td);
        }
        
        // Llamar a registerCalculatorInputs() directamente después de crear los inputs
        registerCalculatorInputs();

        tbody.appendChild(tr);
    }
    tabla.appendChild(tbody);

    // Insertar tabla en el nuevo contenedor
    contenedorGrafico.appendChild(tabla);
    setTimeout(() => {
        registerCalculatorInputs();
        console.log('Inputs registrados después de generar matriz:', document.querySelectorAll('.calculator-input').length);
    }, 0);
}
// Limpiar filas y columnas en el formulario inicial
document.getElementById('limpiar').addEventListener('click', function () {
    numFilasInput.value = '';
    numColumnasInput.value = '';
});
document.addEventListener('DOMContentLoaded', () => {
    console.log('Función registerCalculatorInputs existe:', typeof registerCalculatorInputs === 'function');
    
    const inputs = document.querySelectorAll('.calculator-input');
    console.log('Inputs encontrados:', inputs.length);
});
document.addEventListener("DOMContentLoaded", function () {
    const enviarButton = document.querySelector('.key img[data-funcion="enviar"]').parentElement;

    enviarButton.addEventListener('click', async function() {
        try {
            const filas = document.querySelectorAll('.matrix-table tbody tr');
            if (!filas.length) {
                alert('Por favor, crea una matriz primero');
                return;
            }

            let ecuaciones = [];
            let valoresIniciales = [];

            filas.forEach((fila, index) => {
                const inputs = fila.querySelectorAll('.matrix-input-control');
                let ecuacion = '';
                
                // Construir la ecuación para cada fila
                inputs.forEach((input, colIndex) => {
                    if (colIndex < inputs.length - 1) { // Coeficientes
                        let valor = input.value.trim();
                        // Limpiar el valor de cualquier 'x' o 'y' que pueda contener
                        valor = valor.replace(/[xy]/g, '');
                        
                        if (valor) {
                            // Si el valor es 1, no lo incluimos explícitamente
                            if (valor === '1') {
                                ecuacion += `x${colIndex + 1}`;
                            } else {
                                ecuacion += `${valor}*x${colIndex + 1}`;
                            }
                            
                            if (colIndex < inputs.length - 2) {
                                ecuacion += '+';
                            }
                        } else if (colIndex < inputs.length - 2) {
                            ecuacion = ecuacion.slice(0, -1); // Remover el último '+'
                        }
                    } else { // Término independiente
                        let terminoIndependiente = input.value.trim();
                        terminoIndependiente = terminoIndependiente.replace(/[xy]/g, '');
                        if (terminoIndependiente) {
                            ecuacion += `-${terminoIndependiente}`;
                        }
                    }
                });

                // Añadir la ecuación solo si no está vacía
                if (ecuacion) {
                    ecuaciones.push(ecuacion);
                }
            });

            // Obtener valores iniciales
            const numVariables = filas[0].querySelectorAll('.matrix-input-control').length - 1;
            valoresIniciales = Array(numVariables).fill(1);

            const datos = {
                ecuaciones: ecuaciones.join(','),
                valores_iniciales: valoresIniciales,
                tolerancia: 1e-6,
                max_iteraciones: 100
            };

            console.log('Datos a enviar:', datos);

            const response = await fetch('http://localhost:5100/broyden', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(datos)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Error en la respuesta del servidor');
            }

            const resultado = await response.json();
            console.log('Respuesta del servidor:', resultado);

            if (resultado.converged) {
                let mensaje = 'Solución encontrada:\n';
                resultado.resultado_final.forEach((valor, index) => {
                    mensaje += `x${index + 1} = ${valor.toFixed(6)}\n`;
                });
                alert(mensaje);
            } else {
                alert('El método no convergió después del máximo número de iteraciones');
            }

        } catch (error) {
            console.error('Error:', error);
            alert('Error al procesar la solicitud: ' + error.message);
        }
    });
});