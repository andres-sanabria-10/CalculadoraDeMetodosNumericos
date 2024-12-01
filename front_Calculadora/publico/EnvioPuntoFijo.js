document.addEventListener("DOMContentLoaded", function () {
    const enviarButton = document.querySelector('.key img[data-funcion="enviar"]').parentElement;
    let ggbAPI = null;
    let dataGlobal;

    // Inicializa GeoGebra sin ninguna gráfica
    function inicializarGeoGebra() {
        try {
            const ggbApp = new GGBApplet(
                {
                    appName: "graphing",
                    width: 400,
                    height: 200,
                    showToolBar: false,
                    showAlgebraInput: false,
                    showMenuBar: false,
                    appletOnLoad: function () {
                        ggbAPI = window["ggbApplet"];
                        console.log("GeoGebra cargado correctamente.");
                    }
                },



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
        const calculatorInput = document.getElementById('calculator-input').value;
        const initialPointInput = document.getElementById('initial-point').value;

        const selectedOption = document.querySelector('input[name="options"]:checked');
        const selectedValue = selectedOption ? selectedOption.value : null;


        // Validaciones
        if (!equationInput) {
            alert('Por favor, ingrese la ecuación original.');
            return;
        }
        if (!calculatorInput) {
            alert('Por favor, ingrese la ecuación despejada.');
            return;
        }
        if (!initialPointInput) {
            alert('Por favor, ingrese el punto inicial.');
            return;
        }
        if (!selectedValue) {
            alert('Por favor, seleccione una tolerancia.');
            return;
        }
        const data = {
            Punto_inicial: initialPointInput,
            tolerancia: selectedValue,
            funcion: equationInput,
            transformada: calculatorInput
        };
        console.log('Data a enviar:', data);

        fetch('http://localhost:5201/punto-fijo', {
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

                // Llenar la segunda tabla usando el ID
                const resultadoTableBody = document.getElementById('resultadoTabla').querySelector('tbody');
                resultadoTableBody.innerHTML = ''; // Limpiar el cuerpo de la tabla

                const resultadoRow = document.createElement('tr');
                resultadoRow.innerHTML = `
                    <td>${data["Resultado Final"].toFixed(4)}</td>
                    <td>${data["Número iteraciones"]}</td>
                `;
                resultadoTableBody.appendChild(resultadoRow);




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
            const puntosFuncion = generarPuntosFuncionOriginal(equationInput, xMin, xMax);
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