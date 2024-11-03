// Espera a que el DOM esté completamente cargado
document.addEventListener("DOMContentLoaded", function() {
    // Selecciona el botón
    const enviarButton = document.querySelector('.key img[data-funcion="enviar"]').parentElement;

    // Agrega un event listener al botón
    enviarButton.addEventListener('click', function() {
        // Obtén los valores de los campos de entrada
        const equationInput = document.getElementById('equation-input').value;
        const calculatorInput = document.getElementById('calculator-input').value;
        const initialPointInput = document.getElementById('initial-point').value;

        // Obtén el valor del radio button seleccionado
        const selectedOption = document.querySelector('input[name="options"]:checked');
        const selectedValue = selectedOption ? selectedOption.value : null;

        // Crea un objeto con los datos a enviar
        const data = {
            Punto_inicial: initialPointInput,
            tolerancia: selectedValue,
            funcion: equationInput,
            transformada: calculatorInput
            
            
        };
        console.log('Data a enviar:', data);

        // Envía los datos usando fetch
        fetch('http://localhost:5300/punto-fijo', {
            method: 'POST', // o 'GET' según lo que necesites
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
            // Aquí puedes manejar la respuesta del servidor
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});