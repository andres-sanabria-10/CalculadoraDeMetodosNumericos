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
                    height: 300,
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

                ggbAPI.evalCommand(func); // Graficar la función
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
        // Limpiar la gráfica anterior si es necesario
        if (ggbAPI) {
            ggbAPI.reset(); // Limpia todas las gráficas actuales
        }
        graficarFuncion(equationInput);
    });


    document.getElementById('btnIteraciones').addEventListener('click', function () {
        const equationInput = document.getElementById('equation-input').value;
        const calculatorInput = document.getElementById('calculator-input').value;
        if (!equationInput) {
            alert("Por favor, ingrese una función válida.");
            return;
        }
        // Grafica la función original
        graficarFuncion(equationInput);

        // Graficar la función despejada
        if (calculatorInput) {
            const calculatorEquation = `x = ${calculatorInput}`;
            graficarFuncion(calculatorEquation);
        }

        // Graficar y=x
        if (ggbAPI) {
            ggbAPI.evalCommand('y = x'); // Comando para graficar la función y = x

            console.log("Función y = x graficada.");
        } else {
            console.error("GeoGebra aún no está inicializado.");
        }

        // Luego, agregar los puntos de iteración al gráfico
        // Agregar los puntos de iteración al gráfico
        const colors = [
            [255, 0, 0],   // Rojo
            [0, 255, 0],   // Verde
            [0, 0, 255],   // Azul
            [255, 165, 0], // Naranja
            [128, 0, 128], // Púrpura
            [0, 255, 255], // Cian
            [255, 255, 0]  // Amarillo
        ];

        if (dataGlobal && dataGlobal.Iteraciones) {
            dataGlobal.Iteraciones.forEach((iteracion, index) => {
                try {
                    const x0 = iteracion.X0;

                    // Crear línea vertical en x = X0
                    const lineName = `LineaX0_${index}`;

                    // Crear la línea vertical usando el comando x = valor
                    ggbAPI.evalCommand(`${lineName}: x = ${x0}`);

                    // Seleccionar el color basado en el índice de la iteración
                    const color = colors[index % colors.length];

                    // Configurar la línea con el color seleccionado
                    ggbAPI.setLabelVisible(lineName, false);
                    ggbAPI.setColor(lineName, ...color);  // Asignar el color de la lista
                    ggbAPI.setLineThickness(lineName, 2);

                    // Crear el texto de información (inicialmente oculto)
                    const labelName = `Label_${index}`; // Nombre de la etiqueta basado en el índice
                    const label = `I: ${index}`; // Mostrar el número de la iteración
                    ggbAPI.evalCommand(`${labelName}=Text("${label}", (${x0}, 0))`); // Crear la etiqueta
                    ggbAPI.setVisible(labelName, true); // Hacerla visible


                    // Agregar el evento para mostrar/ocultar el label
                    ggbAPI.registerObjectUpdateListener(lineName, () => {
                        const isMouseOver = ggbAPI.isObjectUnderMouse(lineName);
                        console.log(`Mouse sobre ${lineName}: ${isMouseOver}`);

                        ggbAPI.setVisible(labelName, isMouseOver);
                    });

                } catch (error) {
                    console.error(`Error al procesar iteración ${index}:`, error);
                }
            });
        }

    });

    enviarButton.addEventListener('click', function () {
        const equationInput = document.getElementById('equation-input').value;
        const calculatorInput = document.getElementById('calculator-input').value;
        const initialPointInput = document.getElementById('initial-point').value;

        const selectedOption = document.querySelector('input[name="options"]:checked');
        const selectedValue = selectedOption ? selectedOption.value : null;

        // Graficar la función original

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

            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });

});


