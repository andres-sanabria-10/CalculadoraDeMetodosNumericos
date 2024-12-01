document.addEventListener("DOMContentLoaded", function () {
    const enviarButton = document.querySelector('.key img[data-funcion="enviar"]').parentElement;
    const ctx = document.getElementById('grafico').getContext('2d');
    let chart;

    let xMin = -14, xMax = 18, yMin = -10, yMax = 12;

    function renderChart(data, label) {
        if (chart) chart.destroy();
        chart = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [{
                    label: label,
                    data: data,
                    borderColor: 'rgb(208, 46, 11)',
                    tension: 0.1,
                    pointRadius: 0,
                    borderWidth: 2,
                }],
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
                        grid: { color: 'rgba(0, 0, 0, 0.1)', drawTicks: true },
                        ticks: { stepSize: 2, callback: value => value.toString() },
                    },
                    y: {
                        type: 'linear',
                        position: 'center',
                        min: yMin,
                        max: yMax,
                        grid: { color: 'rgba(0, 0, 0, 0.1)', drawTicks: true },
                        ticks: { stepSize: 2, callback: value => value.toString() },
                    },
                },
                plugins: { legend: { display: true, position: 'top' } },
            },
        });
    }

    document.getElementById('grafico').addEventListener('wheel', function (event) {
        event.preventDefault();
        const zoomFactor = 0.1, delta = event.deltaY;
        if (delta < 0) { xMin += zoomFactor; xMax -= zoomFactor; yMin += zoomFactor; yMax -= zoomFactor; }
        else { xMin -= zoomFactor; xMax += zoomFactor; yMin -= zoomFactor; yMax += zoomFactor; }
        renderChart(chart?.data?.datasets[0]?.data || [], chart?.data?.datasets[0]?.label || '');
    });

    function generarPuntosFuncionOriginal(funcion, min, max, puntos = 100) {
        const datos = [];
        const paso = (max - min) / puntos;
        for (let x = min; x <= max; x += paso) {
            try {
                const y = eval(funcion.replace(/x/g, `(${x})`));
                datos.push({ x, y });
            } catch (error) {
                console.error('Error al evaluar la función:', error);
            }
        }
        return datos;
    }

    enviarButton.addEventListener('click', function () {
        console.log("Enviando datos...");  // Agrega este log para verificar que el evento se dispara

        const equationInput = document.getElementById('equation-input').value.trim();
        const initialPointInput = parseFloat(document.getElementById('initial-point').value);
        const initialPointInput2 = parseFloat(document.getElementById('initial-point2').value);
        const initialPointInput3 = parseInt(document.getElementById('initial-point3').value);

        if (!equationInput || isNaN(initialPointInput) || isNaN(initialPointInput2) || isNaN(initialPointInput3)) {
            alert('Por favor, completa todos los campos correctamente.');
            return;
        }

        const data = {
            a: initialPointInput,
            b: initialPointInput2,
            n: initialPointInput3,
            funcion_str: equationInput,
        };

        fetch('http://localhost:5503/trapecio', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw new Error(err.mensaje || 'Error en el servidor'); });
                }
                return response.json();
            })
            .then(data => {
                console.log('Éxito:', data);
                alert(data.mensaje);

                const resultadoTableBody = document.getElementById('resultadoTabla').querySelector('tbody');
                resultadoTableBody.innerHTML = '';
                const resultadoRow = document.createElement('tr');
                resultadoRow.innerHTML = `
                    <td>${data.area_bajo_la_curva}</td>
                    <td>${data.convergencia}</td>
                    <td>${data.error_relativo}</td>
                `;
                resultadoTableBody.appendChild(resultadoRow);

                // Renderizar el gráfico de la función original
                const puntosFuncion = generarPuntosFuncionOriginal(equationInput, xMin, xMax);
                renderChart(puntosFuncion, 'Función Original');
            })
            .catch(error => {
                console.error('Error:', error);
                alert(`Error al enviar los datos: ${error.message}`);
            });
    });

    document.getElementById('btnFuncionOriginal').addEventListener('click', function () {
        const equationInput = document.getElementById('equation-input').value.trim();
        if (!equationInput) {
            alert('Por favor, ingrese la función para graficar.');
            return;
        }
        const puntosFuncion = generarPuntosFuncionOriginal(equationInput, xMin, xMax);
        renderChart(puntosFuncion, 'Función Original');
    });
});
