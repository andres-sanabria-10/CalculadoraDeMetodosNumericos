const crearButton = document.getElementById('crear');
const numFilasInput = document.getElementById('num_filas');
const numColumnasInput = document.getElementById('num_columnas');
const matrixContainer = document.getElementById('matrixContainer');
const contenedorGrafico = document.querySelector('.scrollable-container');


const iteracionesTabla = document.querySelector('#iteracionesTabla tbody');
const resultadoTabla = document.querySelector('#resultadoTabla tbody');


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

    // Encabezado "Término Independiente"
    const thTerminoIndependiente = document.createElement('th');
    thTerminoIndependiente.innerText = 'Constante';
    headerRow.appendChild(thTerminoIndependiente);

    // Encabezado "Puntos"
    const thPuntos = document.createElement('th');
    thPuntos.innerText = 'Valores\niniciales';
    headerRow.appendChild(thPuntos);



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

        // Inputs para X1, X2, etc.
        for (let j = 0; j < columnas; j++) {
            const td = document.createElement('td');
            const input = document.createElement('input');
            input.type = 'text';
            input.className = 'matrix-input-control matrix-input-size calculator-input';
            input.placeholder = `X${j + 1}`;
            td.appendChild(input);
            tr.appendChild(td);
        }
        // Input para "Término Independiente"
        const tdTerminoIndependiente = document.createElement('td');
        const inputTerminoIndependiente = document.createElement('input');
        inputTerminoIndependiente.type = 'text';
        inputTerminoIndependiente.className = 'matrix-input-control matrix-input-size calculator-input';
        inputTerminoIndependiente.placeholder = 'Constante';
        tdTerminoIndependiente.appendChild(inputTerminoIndependiente);
        tr.appendChild(tdTerminoIndependiente);
        registerCalculatorInputs();

        // Input para "Puntos"
        const tdPuntos = document.createElement('td');
        const inputPuntos = document.createElement('input');
        inputPuntos.type = 'text';
        inputPuntos.className = 'matrix-input-control matrix-input-size calculator-input';
        inputPuntos.placeholder = 'Inicial';
        tdPuntos.appendChild(inputPuntos);
        tr.appendChild(tdPuntos);




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
// Función para limpiar ecuaciones
const limpiarEcuacion = (ecuacion) => ecuacion.replace(/\s+/g, '');

document.addEventListener("DOMContentLoaded", function () {
    const enviarButton = document.querySelector('.key img[data-funcion="enviar"]').parentElement;

    enviarButton.addEventListener('click', async function () {
        try {
            const filas = document.querySelectorAll('.matrix-table tbody tr');
            if (!filas.length) {
                alert('Por favor, crea una matriz primero');
                return;
            }

            let ecuaciones = [];
            let valoresIniciales = [];

            // Recolectar valores iniciales primero
            filas.forEach((fila) => {
                const inputs = fila.querySelectorAll('.matrix-input-control');
                const valorInicial = inputs[inputs.length - 1].value.trim() || '0';
                if (isNaN(valorInicial)) {
                    throw new Error('Valor inicial no válido en una de las filas');
                }
                valoresIniciales.push(parseFloat(valorInicial));
            });

            // Recolectar ecuaciones (excluyendo el valor inicial)
            filas.forEach((fila) => {
                const inputs = fila.querySelectorAll('.matrix-input-control');
                let ecuacion = '';

                // Excluir el último input (valor inicial)
                inputs.forEach((input, index) => {
                    if (index < inputs.length - 1) {
                        const valor = input.value.trim();
                        if (valor) {
                            if (ecuacion) ecuacion += ' + '; // Separador entre términos
                            ecuacion += valor;
                        }
                    }
                });

                // Añadir la ecuación solo si no está vacía
                if (ecuacion) {
                    ecuaciones.push(ecuacion);
                }
            });

            // Limpiar las ecuaciones recolectadas
            ecuaciones = ecuaciones.map(limpiarEcuacion);

            if (ecuaciones.length !== valoresIniciales.length) {
                throw new Error(`Número de ecuaciones (${ecuaciones.length}) no coincide con los valores iniciales (${valoresIniciales.length}).`);
            }

            const datos = {
                ecuaciones: ecuaciones.join(','), // Se envían las ecuaciones como texto separado por comas
                valores_iniciales: valoresIniciales,
                tolerancia: 1e-6,
                max_iteraciones: 100
            };

            console.log('Datos a enviar:', datos);
            ecuaciones.forEach((ecuacion, index) => {
                console.log(`Ecuación ${index + 1}:`, ecuacion);
            });

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
                let mensaje = 'El método converge';
                resultado.resultado_final.forEach((valor, index) => {
                    mensaje += `x${index + 1} = ${valor.toFixed(6)}\n`;
                });
                alert(mensaje);
                iteracionesTabla.innerHTML = '';
                resultadoTabla.innerHTML = '';

                // Llenar la tabla de iteraciones
                if (Array.isArray(data.iteraciones)) {
                    data.iteraciones.forEach(iteracion => {
                        const newRow = document.createElement('tr');
                        newRow.innerHTML = `
            <td>${iteracion.iteracion || '---'}</td>
            <td>${iteracion.V !== undefined ? iteracion.V.map(v => v.toFixed(4)).join(', ') : '---'}</td>
            <td>${iteracion.error !== undefined && !isNaN(iteracion.error) ? iteracion.error.toFixed(4) : '---'}</td>
        `;
                        iteracionesTabla.appendChild(newRow);
                    });
                } else {
                    console.error("La propiedad 'iteraciones' no está definida o no es un array.");
                }

                // Llenar la tabla de resultados finales
                if (data.resultado_final && typeof data.numero_iteraciones !== 'undefined') {
                    const resultadoRow = document.createElement('tr');
                    resultadoRow.innerHTML = `
        <td>${data.resultado_final.map(v => v.toFixed(4)).join(', ')}</td>
        <td>${data.numero_iteraciones}</td>
    `;
                    resultadoTabla.appendChild(resultadoRow);
                } else {
                    console.error("Los datos de 'resultado_final' o 'numero_iteraciones' no están definidos.");
                }




            } else {
                alert('El método no convergió después del máximo número de iteraciones');
            }

        } catch (error) {
            console.error('Error:', error);
            alert('Error al procesar la solicitud: ' + error.message);
        }
    });
});
