document.addEventListener("DOMContentLoaded", function () {
    const enviarButton = document.querySelector('.key img[data-funcion="enviar"]').parentElement;
    const ctx = document.getElementById('grafico').getContext('2d');
    let chart;
    let dataGlobal;

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
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1,
                    pointRadius: 0, // Remove points
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: 'linear',
                        position: 'center', // This will make the axis cross at zero
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)',
                            drawTicks: true
                        },
                        ticks: {
                            stepSize: 2,
                            callback: function (value) {
                                return value.toString();
                            }
                        },
                        min: -14,
                        max: 18
                    },
                    y: {
                        type: 'linear',
                        position: 'center', // This will make the axis cross at zero
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)',
                            drawTicks: true
                        },
                        ticks: {
                            stepSize: 2,
                            callback: function (value) {
                                return value.toString();
                            }
                        },
                        min: -10,
                        max: 12
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
        const calculatorInput = document.getElementById('calculator-input').value;
        const initialPointInput = document.getElementById('initial-point').value;

        const selectedOption = document.querySelector('input[name="options"]:checked');
        const selectedValue = selectedOption ? selectedOption.value : null;

        const data = {
            Punto_inicial: initialPointInput,
            tolerancia: selectedValue,
            funcion: equationInput,
            transformada: calculatorInput
        };
        console.log('Data a enviar:', data);

        fetch('http://localhost:5300/punto-fijo', {
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

                dataGlobal = data;

                // Llenar la tabla
                const tableBody = document.querySelector('.table tbody');
                tableBody.innerHTML = '';

                data.Iteraciones.forEach(iteracion => {
                    const newRow = document.createElement('tr');
                    newRow.innerHTML = `
                    <td>${iteracion.Iteración}</td>
                    <td>${iteracion.X0.toFixed(4)}</td>
                    <td>${iteracion.X0_nuevo.toFixed(4)}</td>
                    <td>${iteracion.error.toFixed(4)}</td>
                    <td>${iteracion.valor_funcion.toFixed(4)}</td>
                `;
                    tableBody.appendChild(newRow);
                });

                // Mostrar inicialmente el gráfico de iteraciones
                const iteracionesData = data.Iteraciones.map(iteracion => ({
                    x: iteracion.X0,
                    y: iteracion.valor_funcion
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
            // Generar puntos para la función original
            // Puedes ajustar el rango según tus necesidades
            const puntosFuncion = generarPuntosFuncionOriginal(equationInput, -10, 10);
            renderChart(puntosFuncion, 'Función Original');
        }
    });

    // Evento para el botón de Iteraciones
    document.getElementById('btnIteraciones').addEventListener('click', function () {
        if (dataGlobal && dataGlobal.Iteraciones) {
            const iteracionesData = dataGlobal.Iteraciones.map(iteracion => ({
                x: iteracion.X0,
                y: iteracion.valor_funcion
            }));
            renderChart(iteracionesData, 'Iteraciones');
        }
    });
});