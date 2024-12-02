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
        if (!equationInput) {
            alert("Por favor, ingrese una función válida.");
            return;
        }

        graficarFuncion(equationInput);

        if (dataGlobal && dataGlobal.iteraciones) {
            
            // Graficar las iteraciones
            const colors = [
                [255, 0, 0],   // Rojo
                [0, 255, 0],   // Verde
                [0, 0, 255],   // Azul
                [255, 165, 0], // Naranja
                [128, 0, 128], // Púrpura
                [0, 255, 255], // Cian
                [255, 255, 0]  // Amarillo
            ];
            

            // Iterar sobre las iteraciones y graficar los puntos
            dataGlobal.iteraciones.forEach((iteracion, index) => {
                const x_i = iteracion.x_i;
                const pointName = `Punto_${index}`;

                // Graficar el punto 
                ggbAPI.evalCommand(`${pointName} = (${x_i}, 0)`);
                ggbAPI.evalCommand(`SetPointSize(${pointName}, 4)`);
                ggbAPI.evalCommand(`SetColor(${pointName}, ${colors[index % colors.length].join(', ')})`);
                ggbAPI.evalCommand(`ShowLabel(${pointName}, false)`);

                // Graficar la línea vertical 
                const lineName = `Linea_${index}`;
                ggbAPI.evalCommand(`${lineName}: x = ${x_i}`);
                const color = colors[index % colors.length];
                ggbAPI.setLabelVisible(lineName, false);
                ggbAPI.setColor(lineName, ...color);                              
                ggbAPI.setLineThickness(lineName, 2);

                // Crear texto de información (iteración)
                const labelName = `Label_${index}`;
                const label = `I: ${index + 1}`;
                ggbAPI.evalCommand(`${labelName} = Text("${label}", (${x_i}, 0))`);
                ggbAPI.setVisible(labelName, true);

                // Hacer visible la etiqueta al pasar el mouse por encima de la línea
                ggbAPI.registerObjectUpdateListener(lineName, () => {
                    const isMouseOver = ggbAPI.isObjectUnderMouse(lineName);
                    ggbAPI.setVisible(labelName, isMouseOver);
                });
            });

            console.log("Puntos añadidos");
        }
        
    });

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