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

    function crearFuncionEvaluadora(funcionStr) {
        try {
            return new Function('x', `return ${funcionStr};`);
        } catch (error) {
            console.error('Error al crear la función evaluadora:', error);
            return null;
        }
    }

    
    function generarPuntosIteraciones(iteraciones, evaluador) {
        const puntosGenerados = [];
        console.log("Iteraciones proporcionadas:", iteraciones);
        iteraciones.forEach(iteracion => {
            try {
                console.log(`Evaluando iteración en X0 = ${iteracion.X0}`);
                const yFuncion = evaluador(iteracion.X0); // Evaluar la función en el punto X0
                if (isFinite(yFuncion)) {
                    puntosGenerados.push({ x: iteracion.X0, y: yFuncion });
                } else {
                    console.warn(`Valor no finito en iteración X0=${iteracion.X0}`);
                }
            } catch (error) {
                console.error(`Error al evaluar iteración en X0=${iteracion.X0}:`, error);
            }
        });
        return puntosGenerados;
    }  

    function generarPuntosFuncionOriginal(funcion, min, max, puntos , iteracionesData = []) {
        const datos = [];
        const paso = (max - min) / puntos;
        const evaluador = crearFuncionEvaluadora(funcion);
    
        if (!evaluador) {
            console.error('No se pudo crear la función evaluadora.');
            return datos;
        }
    
        // Generar los puntos de la función original
        for (let x = min; x <= max; x += paso) {
            try {
                const y = evaluador(x);
                if (isFinite(y)) {
                    datos.push({ x, y });
                } else {
                    console.warn(`Valor no finito en x=${x}: y=${y}`);
                }
            } catch (error) {
                console.error(`Error al evaluar la función en x=${x}:`, error);
            }
        }
    
        // Agregar puntos de iteración, eliminando duplicados
        const puntosUnicos = new Set(datos.map(p => `${p.x.toFixed(4)},${p.y.toFixed(4)}`)); // Normalizar precisión
        iteracionesData.forEach(iteracion => {
            try {
                const yFuncion = evaluador(iteracion.X0);
                if (isFinite(yFuncion)) {
                    const punto = `${iteracion.X0.toFixed(4)},${yFuncion.toFixed(4)}`;
                    if (!puntosUnicos.has(punto)) {
                        puntosUnicos.add(punto);
                        datos.push({ x: iteracion.X0, y: yFuncion });
                    }
                } else {
                    console.warn(`Valor no finito en X0=${iteracion.X0}`);
                }
            } catch (error) {
                console.error(`Error al evaluar iteración en X0=${iteracion.X0}:`, error);
            }
        });

        datos.sort((a, b) => a.x - b.x);
    
        console.log("Datos finales para renderizar el gráfico:", datos);
        return datos;
    }
    

    function renderChartCombinado(funcionData, iteracionesData, funcion) {
        if (chart) {
            chart.destroy();
        }
    
        const verticalLines = iteracionesData.flatMap(iteracion => {
            try {
                const yFuncionOriginal = eval(funcion.replace(/x/g, `(${iteracion.x})`));
                

                return [
                    { x: iteracion.x, y: iteracion.y }, 
                    { x: iteracion.x, y: yFuncionOriginal } 
                ];
            } catch (error) {
                console.error(`Error al evaluar la función en x=${iteracion.x}:`, error);
                return []; 
            }
        });


        chart = new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [
                    {
                        type: 'line',
                        label: 'Función Original',
                        data: funcionData,
                        borderColor: 'rgb(208, 46, 11)',
                        tension: 0.1,
                        pointRadius: 3,
                        borderWidth: 2
                    },
                    {
                        type: 'scatter',
                        label: 'Iteraciones',
                        data: iteracionesData,
                        backgroundColor: 'rgb(0, 123, 255)',
                        pointRadius: 5
                    },
                    {
                        type: 'line',
                        label: 'Proyecciones',
                        data: verticalLines,
                        borderColor: 'rgb(0, 123, 255)', 
                        borderDash: [5, 5], 
                        borderWidth: 2,
                        showLine: true,
                        pointRadius: 0, 
                        stepped: false, 
                        spanGaps: true 
                    }
                    
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { type: 'linear' },
                    y: { type: 'linear' }
                },
                plugins: {
                    legend: { display: true },
                    zoom: {
                        pan: { enabled: true, mode: 'xy' },
                        zoom: {
                            wheel: { enabled: true },
                            pinch: { enabled: true },
                            mode: 'xy'
                        }
                    }
                }
            }
        });
    }
    

    // Evento para el botón de Función Original
    document.getElementById('btnFuncionOriginal').addEventListener('click', function () {
        if (dataGlobal) {
            const equationInput = document.getElementById('equation-input').value;
            const puntosFuncion = generarPuntosFuncionOriginal(equationInput, xMin, xMax, 250);
            renderChartCombinado(puntosFuncion, []);
        }
    });

    document.getElementById('btnIteraciones').addEventListener('click', function () {
        if (dataGlobal && dataGlobal.Iteraciones) {
            const iteracionesData = dataGlobal.Iteraciones.map(iteracion => ({
                x: iteracion.X0,
                y: iteracion.valor_funcion
            }));
            const equationInput = document.getElementById('equation-input').value;
            const puntosFuncion = generarPuntosFuncionOriginal(equationInput, xMin, xMax);
            renderChartCombinado(puntosFuncion, iteracionesData, equationInput); 
        }
    });

    // Evento para enviar los datos
    enviarButton.addEventListener('click', function () {
        const equationInput = document.getElementById('equation-input').value;
        const calculatorInput = document.getElementById('calculator-input').value;
        const initialPointInput = document.getElementById('initial-point').value;

        const selectedOption = document.querySelector('input[name="options"]:checked');
        const selectedValue = selectedOption ? selectedOption.value : null;

        if (!equationInput || !calculatorInput || !initialPointInput || !selectedValue) {
            alert('Por favor, complete todos los campos y seleccione una tolerancia.');
            return;
        }

        const data = {
            Punto_inicial: initialPointInput,
            tolerancia: selectedValue,
            funcion: equationInput,
            transformada: calculatorInput
        };

        fetch('http://localhost:5201/punto-fijo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Éxito:', data);
            alert(data.mensaje);

            dataGlobal = data;

            // Actualizar tabla de iteraciones
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

            // Actualizar tabla de resultados
            const resultadoTableBody = document.getElementById('resultadoTabla').querySelector('tbody');
            resultadoTableBody.innerHTML = '';
            const resultadoRow = document.createElement('tr');
            resultadoRow.innerHTML = `
                <td>${data["Resultado Final"].toFixed(4)}</td>
                <td>${data["Número iteraciones"]}</td>
            `;
            resultadoTableBody.appendChild(resultadoRow);

            // Mostrar gráfico combinado
            const puntosFuncion = generarPuntosFuncionOriginal(equationInput, xMin, xMax, 250, data.Iteraciones);
            const iteracionesData = data.Iteraciones.map(iteracion => ({
                x: iteracion.X0,
                y: iteracion.valor_funcion
            }));
            renderChartCombinado(puntosFuncion, iteracionesData, equationInput);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});
