document.addEventListener("DOMContentLoaded", function () {
    const enviarButton = document.querySelector('.key img[data-funcion="enviar"]').parentElement;

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
                if (!response.ok) {
                    throw new Error('Error en la red');
                }
                return response.json();
            })
            .then(data => {
                console.log('Éxito:', data);
                // Llenar la tabla con los resultados
                const tableBody = document.querySelector('.table tbody');
                tableBody.innerHTML = ''; // Limpiar la tabla antes de llenarla

                data.Iteraciones.forEach(iteracion => {
                    const newRow = document.createElement('tr');
                    newRow.innerHTML = `
                    <td>${iteracion.Iteración}</td>
                    <td>${iteracion.X0.toFixed(4)}</td> <!-- Formatear a 4 decimales -->
                    <td>${iteracion.X0_nuevo.toFixed(4)}</td> <!-- Formatear a 4 decimales -->
                    <td>${iteracion.error.toFixed(4)}</td> <!-- Formatear a 4 decimales -->
                    <td>${iteracion.valor_funcion.toFixed(4)}</td> <!-- Formatear a 4 decimales -->
                `;
                    tableBody.appendChild(newRow);
                });
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });
});