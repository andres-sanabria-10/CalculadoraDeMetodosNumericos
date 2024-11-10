document.addEventListener("DOMContentLoaded", function () {
    const enviarButton = document.querySelector('.key img[data-funcion="enviar"]').parentElement;
    enviarButton.addEventListener('click', function () {
        const equationInput = document.getElementById('equation-input').value;
        const initialPointInput = document.getElementById('initial-point').value;
        const selectedOption = document.querySelector('input[name="options"]:checked');
        const selectedValue = selectedOption ? selectedOption.value : null;

        // Validaciones
        if (!equationInput) {
            alert('Por favor, ingrese la ecuación original.');
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
            punto_inicial: initialPointInput,
            tolerancia: selectedValue,
            funcion: equationInput,
        };
        console.log('Data a enviar:', data);

        fetch('http://localhost:5200/newton-raphson', {
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

                // Llenar la tabla de iteraciones
                const tableBody = document.querySelector('#iteracionesTabla tbody');
                tableBody.innerHTML = '';

                // Verifica si data.iteraciones está definido y es un array
                if (Array.isArray(data.iteraciones)) {
                    data.iteraciones.forEach(iteracion => {
                        const newRow = document.createElement('tr');
                        newRow.innerHTML = `
                            <td>${iteracion.iteracion}</td>
                            <td>${iteracion.x_i.toFixed(4)}</td>
                            <td>${iteracion.diferencia.toFixed(4)}</td>
                            <td>${iteracion.g_prima.toFixed(4)}</td>
                            <td>${(iteracion.error * 100).toFixed(4)}%</td> <!-- Multiplicado por 100 para porcentaje -->
                        `;
                        tableBody.appendChild(newRow);
                    });
                } else {
                    console.error('data.iteraciones no está definido o no es un array:', data.iteraciones);
                    alert('No se encontraron iteraciones. Verifique la entrada.');
                }

                // Llenar la tabla de resultados
                const resultadoTableBody = document.getElementById('resultadoTabla').querySelector('tbody');
                resultadoTableBody.innerHTML = ''; // Limpiar el cuerpo de la tabla

                const resultadoRow = document.createElement('tr');
                resultadoRow.innerHTML = `
                <td>${data["resultado_final"].toFixed(4)}</td>
                <td>${data["numero_iteraciones"]}</td>
            `;
                resultadoTableBody.appendChild(resultadoRow);

                
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });
});