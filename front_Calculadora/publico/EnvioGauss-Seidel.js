const crearButton = document.getElementById('crear');
const numFilasInput = document.getElementById('num_filas');
const numColumnasInput = document.getElementById('num_columnas');
const matrixContainer = document.getElementById('matrixContainer');
const contenedorGrafico = document.querySelector('.scrollable-container');

// Obtener el valor seleccionado
const selectedOption = document.querySelector('input[name="options"]:checked');

// Verificar si hay una opción seleccionada
const selectedValue = selectedOption ? selectedOption.value : null;



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

    // Encabezado del símbolo "="
    const thIgual = document.createElement('th');
    thIgual.innerText = '=';
    headerRow.appendChild(thIgual);

    // Encabezado "Término Independiente"
    const thTerminoIndependiente = document.createElement('th');
    thTerminoIndependiente.innerText = 'Constante';
    headerRow.appendChild(thTerminoIndependiente);





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

        // Celda del símbolo "="
        const tdIgual = document.createElement('td');
        tdIgual.className = 'matrix-symbol';
        tdIgual.innerText = '=';
        tr.appendChild(tdIgual);

        // Input para "Término Independiente"
        const tdTerminoIndependiente = document.createElement('td');
        const inputTerminoIndependiente = document.createElement('input');
        inputTerminoIndependiente.type = 'text';
        inputTerminoIndependiente.className = 'matrix-input-control matrix-input-size calculator-input';
        inputTerminoIndependiente.placeholder = 'Constante';
        tdTerminoIndependiente.appendChild(inputTerminoIndependiente);
        tr.appendChild(tdTerminoIndependiente);
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
// Función para limpiar ecuaciones
const limpiarEcuacion = (ecuacion) => ecuacion.replace(/\s+/g, '');

document.addEventListener("DOMContentLoaded", function () {
    const enviarButton = document.querySelector('.key img[data-funcion="enviar"]').parentElement;

    enviarButton.addEventListener('click', async function () {
        try {
            // Obtener el valor seleccionado para la tolerancia
            const selectedOption = document.querySelector('input[name="options"]:checked');
            const selectedValue = selectedOption ? selectedOption.value : null;

            // Verificar si se ha seleccionado una opción de tolerancia
            if (!selectedValue) {
                alert("Por favor, selecciona una tolerancia.");
                return; // Salir de la función si no se ha seleccionado una opción
            }

            const filas = document.querySelectorAll('.matrix-table tbody tr');
            if (!filas.length) {
                alert('Por favor, crea una matriz primero');
                return;
            }

            let ecuaciones = [];

            // Recolectar ecuaciones y valores iniciales
            filas.forEach((fila) => {
                const inputs = fila.querySelectorAll('.matrix-input-control');
                let ecuacion = '';
                const constante = inputs[inputs.length - 1].value.trim();

                // Validar constante
                if (isNaN(constante) || constante === '') {
                    throw new Error('Constante no válida en una de las filas.');
                }

                // Construir ecuación
                inputs.forEach((input, index) => {
                    if (index < inputs.length - 1) {
                        const valor = input.value.trim();
                        if (valor) {
                            const signo = valor.startsWith('-') ? '' : '+ ';
                            ecuacion += `${signo}${valor} `;
                        }
                    }
                });

                ecuacion += `= ${constante}`;
                ecuaciones.push(ecuacion.trim());
            });

            const toleranciaAca = parseFloat(selectedValue);

            // Verificar si la conversión fue exitosa
            if (isNaN(toleranciaAca)) {
                alert("El valor de tolerancia debe ser un número válido.");
                return; // Salir de la función si el valor de tolerancia no es un número
            }

            // Datos para enviar al backend
            const datos = {
                ecuaciones: ecuaciones, // Lista de ecuaciones unidas
                tolerancia: toleranciaAca, // Valor de la tolerancia seleccionado
                max_iteraciones: 100 // Número máximo de iteraciones
            };


            console.log('Datos a enviar:', datos);

            // Enviar datos al backend
            const response = await fetch('http://localhost:5502/gauss-seidel', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(datos)
            });

            if (!response.ok) {
                const errorData = await response.json();
                alert(`Error del servidor ${errorData.mensaje}`);
            }

            const resultado = await response.json();
            console.log('Respuesta del servidor:', resultado);

            if (resultado.converged) {
                let mensaje = 'El método converge:\n';
                resultado.resultado_final.forEach((valor, index) => {
                    mensaje += `x${index + 1} = ${valor.toFixed(6)}\n`;
                });
                alert(mensaje);
                // Renderizar iteraciones y resultados
                llenarTablaIteraciones(resultado.iteraciones);
                llenarTablaResultados(resultado.resultado_final, resultado.numero_iteraciones);


            } else {
                alert('El método no convergió después del máximo número de iteraciones.');
            }

        } catch (error) {
            console.error('Error:', error);
            alert('Error al procesar la solicitud: ' + error.message);
        }
    });

 
// Función para llenar la tabla de iteraciones
function llenarTablaIteraciones(iteraciones) {
    const iteracionesTablaBody = document.querySelector('#iteracionesTabla tbody');
    iteracionesTablaBody.innerHTML = ''; // Limpiar la tabla de iteraciones

    if (Array.isArray(iteraciones)) {
        iteraciones.forEach(iteracion => {
            const newRow = document.createElement('tr');
            newRow.innerHTML = `
                <td>${iteracion.iteracion || '---'}</td>
                <td>${iteracion.solucion.map(v => v.toFixed(6)).join('<br>') || '---'}</td>
                <td>${iteracion.error !== undefined ? (iteracion.error * 100).toFixed(6) + '%' : '---'}</td>
            `;
            iteracionesTablaBody.appendChild(newRow);
        });
    } else {
        console.error("La propiedad 'iteraciones' no está definida o no es un array.");
    }
}

// Función para llenar la tabla de resultados finales
function llenarTablaResultados(resultadoFinal, numeroIteraciones) {
    const resultadoTablaBody = document.querySelector('#resultadoTabla tbody');
    resultadoTablaBody.innerHTML = ''; // Limpiar la tabla de resultados

    if (resultadoFinal && typeof numeroIteraciones !== 'undefined') {
        const resultadoRow = document.createElement('tr');
        resultadoRow.innerHTML = `
            <td>${resultadoFinal.map(v => v.toFixed(6)).join('<br>')}</td>
            <td>${numeroIteraciones}</td>
        `;
        resultadoTablaBody.appendChild(resultadoRow);
    } else {
        console.error("Los datos de 'resultado_final' o 'numero_iteraciones' no están definidos.");
    }
}







   
});
