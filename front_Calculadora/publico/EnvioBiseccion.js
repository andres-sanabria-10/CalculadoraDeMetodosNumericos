document.addEventListener("DOMContentLoaded", function () {
    const enviarButton = document.querySelector('.key img[data-funcion="enviar"]').parentElement;
    const ctx = document.getElementById('grafico').getContext('2d');
    let chart;
    let dataGlobal;

    // Límites iniciales para los ejes
    let xMin = -14;
    let xMax = 18;
    let yMin = -10;
    let yMax = 12;

    let chartFuncionOriginal;
    let chartIteraciones;
    
    function renderChart(chart, data, label, canvasId) {
        if (chart) {
            chart.destroy(); // Eliminar el gráfico anterior
        }
    
        const ctx = document.getElementById(canvasId).getContext('2d');
    
        chart = new Chart(ctx, {
            type: 'scatter', // Tipo de gráfico scatter (solo puntos)
            data: {
                datasets: [{
                    label: label,
                    data: data, // Los puntos de iteración (coordenadas x, y)
                    backgroundColor: label === 'Función Original' ? 'orange' : 'blue', // Diferenciar los colores
                    borderColor: label === 'Función Original' ? 'orange' : 'blue',
                    pointRadius: 5, // Tamaño de los puntos
                    pointHoverRadius: 7, // Tamaño de los puntos al pasar el cursor (opcional)
                    showLine: false, // Asegurarse de que no haya líneas entre los puntos
                    borderWidth: 2 // Ancho del borde de los puntos
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: 'linear',
                        position: 'bottom',
                        min: xMin,
                        max: xMax,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)',
                            drawTicks: true
                        },
                        ticks: {
                            stepSize: 2,
                            callback: function (value) {
                                return value.toString();
                            }
                        }
                    },
                    y: {
                        type: 'linear',
                        position: 'left',
                        min: yMin,
                        max: yMax,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)',
                            drawTicks: true
                        },
                        ticks: {
                            stepSize: 2,
                            callback: function (value) {
                                return value.toString();
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                }
            }
        });
    }
    

    // Evento para zoom con la rueda del mouse
    document.getElementById('grafico').addEventListener('wheel', function (event) {
        event.preventDefault(); // Evita el desplazamiento de la página al hacer zoom

        const zoomFactor = 0.1; // Factor de zoom
        const delta = event.deltaY;

        if (delta < 0) { // Zoom in
            xMin += zoomFactor;
            xMax -= zoomFactor;
            yMin += zoomFactor;
            yMax -= zoomFactor;
        } else { // Zoom out
            xMin -= zoomFactor;
            xMax += zoomFactor;
            yMin -= zoomFactor;
            yMax += zoomFactor;
        }

        renderChart(chart.data.datasets[0].data, chart.data.datasets[0].label);
    });


    function generarPuntosFuncionOriginal(funcion, min, max, puntos = 100) {
        const datos = [];
        const paso = (max - min) / puntos;
    
        for (let x = min; x <= max; x += paso) {
            try {
                const y = eval(funcion.replace(/x/g, `(${x})`));
                datos.push({ x: x, y: y });
            } catch (error) {
                console.error('Error al evaluar la función:', error);
            }
        }
        return datos;
    }


    enviarButton.addEventListener('click', function () {
        const equationInput = document.getElementById('equation-input').value;

        const initialPointInput = document.getElementById('initial-point').value;
        const initialPointInput2 = document.getElementById('initial-point2').value;
        const selectedOption = document.querySelector('input[name="options"]:checked');
        const selectedValue = selectedOption ? selectedOption.value : null;


        // Validaciones
        if (!equationInput) {
            alert('Por favor, ingrese la ecuación original.');
            return;
        }
        if (!initialPointInput2) {
            alert('Por favor, ingrese el segundo punto Inicial B.');
            return;
        }
        if (!initialPointInput) {
            alert('Por favor, ingrese el punto inicial A.');
            return;
        }
        if (!selectedValue) {
            alert('Por favor, seleccione una tolerancia.');
            return;
        }
        const data = {
            punto_inicial_a: initialPointInput,
            punto_inicial_b: initialPointInput2,
            tolerancia: selectedValue,
            funcion: equationInput
        };
        console.log('Data a enviar:', data);

        fetch('http://localhost:5800/biseccion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(response => {
                return response.json().then(data => {
                    if (!response.ok) {
                        alert(data.mensaje || 'Ocurrió un error en el cálculo');
                        throw new Error(data.error || 'Error en el cálculo');
                    }
                    return data;
                });
            })
            .then(data => {
                console.log('Éxito:', data);
                alert(data.mensaje);

                // Llenar la tabla de iteraciones
                const iteracionesTableBody = document.querySelector('.table tbody');
                iteracionesTableBody.innerHTML = ''; // Limpiar la tabla antes de llenarla

                // Asegúrate de que `data.Iteraciones` existe y es un array
                if (Array.isArray(data.Iteraciones)) {
                    data.Iteraciones.forEach(iteracion => {
                        const newRow = document.createElement('tr');
                        newRow.innerHTML = `
                            <td>${iteracion.Iteración}</td>
                            <td>${iteracion.PuntoA.toFixed(4)}</td>
                            <td>${iteracion.PuntoB.toFixed(4)}</td>
                            <td>${iteracion.PuntoMedio.toFixed(4)}</td>
                            <td>${iteracion.ErrorPorcentual.toFixed(4)}</td>
                        `;
                        iteracionesTableBody.appendChild(newRow);
                    });
                }

                // Llenar la tabla de resultados finales
                const resultadoTableBody = document.getElementById('resultadoTabla').querySelector('tbody');
                resultadoTableBody.innerHTML = ''; // Limpiar la tabla antes de llenarla

                // Asegúrate de que `data["Resultado Final"]` y `data["Número de iteraciones"]` existen
                const resultadoRow = document.createElement('tr');
                resultadoRow.innerHTML = `
                    <td>${data["resultado_final"].toFixed(4)}</td>
                    <td>${data["numero_iteraciones"]}</td>
                `;
                resultadoTableBody.appendChild(resultadoRow);

                // Renderizar el gráfico de iteraciones
                const iteracionesData = data.Iteraciones.map(iteracion => ({
                    x: iteracion.PuntoMedio, // Aquí debes ajustar según lo que quieras graficar
                    y: iteracion.ErrorPorcentual // Aquí también
                }));
                renderChart(iteracionesData, 'Iteraciones');
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });

    // Evento para el botón de Función Original
    document.getElementById('btnFuncionOriginal').addEventListener('click', function () {
        const equationInput = document.getElementById('equation-input').value;
    
        if (!equationInput) {
            alert('Por favor, ingrese una ecuación válida.');
            return;
        }
    
        const puntosFuncion = generarPuntosFuncionOriginal(equationInput, xMin, xMax);
        renderChart(puntosFuncion, 'Función Original');
    });
    


});