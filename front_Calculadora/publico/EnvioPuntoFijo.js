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
                true
            );
            ggbApp.inject('ggb-element');
        } catch (error) {
            console.error("Error al inicializar GeoGebra:", error);
        }
    }

    // Agrega una función a GeoGebra
    function graficarFuncion(func) {
        try {
            if (ggbAPI) {
                ggbAPI.reset(); // Limpia el canvas antes de graficar
                ggbAPI.evalCommand(func);
                console.log(`Función graficada: ${func}`);
            } else {
                console.error("GeoGebra aún no está inicializado.");
            }
        } catch (error) {
            console.error("Error al graficar la función en GeoGebra:", error);
        }
    }

    inicializarGeoGebra();

    // Manejar clic en el botón "Función Original"
    document.getElementById('btnFuncionOriginal').addEventListener('click', function () {
        const equationInput = document.getElementById('equation-input').value;
        if (!equationInput) {
            alert("Por favor, ingrese una función válida.");
            return;
        }
        graficarFuncion(equationInput);
    });

    document.getElementById('btnIteraciones').addEventListener('click', function () {
        const equationInput = document.getElementById('equation-input').value;
        if (!equationInput) {
            alert("Por favor, ingrese una función válida.");
            return;
        }

        // Grafica la función original
        graficarFuncion(equationInput);

        // Luego, agregar los puntos de iteración al gráfico
        if (dataGlobal && dataGlobal.Iteraciones) {
            dataGlobal.Iteraciones.forEach((iteracion, index) => {
                const x0 = iteracion.X0;
                const x0Nuevo = iteracion.X0_nuevo;
                const y0 = iteracion.valor_funcion;
            
                const pointNameX0 = `PuntoX0_${index}`;
                const pointNameX0Nuevo = `PuntoX0Nuevo_${index}`;
            
                // Crear los puntos
                ggbAPI.evalCommand(`${pointNameX0} = (${x0}, ${y0})`);
                ggbAPI.evalCommand(`${pointNameX0Nuevo} = (${x0Nuevo}, 0)`);

                // Hacer visuales los puntos
                ggbAPI.evalCommand(`SetPointSize(${pointNameX0}, 4)`);
                ggbAPI.evalCommand(`SetColor(${pointNameX0}, 255, 0, 0)`); 
                ggbAPI.evalCommand(`SetPointSize(${pointNameX0Nuevo}, 4)`);
                ggbAPI.evalCommand(`SetColor(${pointNameX0Nuevo}, 0, 0, 255)`); 


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