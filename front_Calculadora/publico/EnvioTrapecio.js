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



    function renderChart(data, label) {
        if (chart) {
            chart.destroy();
        }
        chart = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [{
                    label: label,
                    data: data,
                    borderColor: 'rgb(208, 46, 11)',
                    tension: 0.1,
                    pointRadius: 0,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: 'linear',
                        position: 'center',
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
                        position: 'center',
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
                // Usar math.js o una biblioteca similar para evaluar la función
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
        const initialPointInput3 = document.getElementById('initial-point3').value;
        const selectedOption = document.querySelector('input[name="options"]:checked');
        const selectedValue = selectedOption ? selectedOption.value : null;


        // Validaciones
        if (!equationInput) {
            alert('Por favor, ingrese la función.');
            return;
        }
        if (!initialPointInput3) {
            alert('Por favor, ingrese el numero de subintervalos (n).');
            return;
        }

        if (!initialPointInput2) {
            alert('Por favor, ingrese el primer valor del intervalo (b).');
            return;
        }
        if (!initialPointInput) {
            alert('Por favor, ingrese el segundo valor del intervalo (a).');
            return;
        }

        if (!selectedValue) {
            alert('Por favor, seleccione una tolerancia.');
            return;
        }
        const data = {
            a: initialPointInput,
            b: initialPointInput2,
            n: initialPointInput3,
            tolerancia: selectedValue,
            funcion: equationInput
        };
        console.log('Data a enviar:', data);

        fetch('http://localhost:5503/trapecio', {
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
                const iteracionesData = data.iteraciones.map(iteracion => ({
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
        if (dataGlobal) {
            const equationInput = document.getElementById('equation-input').value;
            const puntosFuncion = generarPuntosFuncionOriginal(equationInput, xMin, xMax);
            renderChart(puntosFuncion, 'Función Original');
        }
    });


});