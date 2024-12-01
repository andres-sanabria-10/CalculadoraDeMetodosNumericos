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

        // Primero, graficar la función original
        graficarFuncion(equationInput);

        // Luego, agregar los puntos de iteración al gráfico
        if (dataGlobal && dataGlobal.Iteraciones) {
            dataGlobal.Iteraciones.forEach((iteracion, index) => {
                const x0 = iteracion.X0;
                const x0Nuevo = iteracion.X0_nuevo;
                const y0 = iteracion.valor_funcion;

                // Poner el punto X0 sobre la función original
                const pointNameX0 = `PuntoX0_${index}`;
                ggbAPI.evalCommand(`${pointNameX0} = (${x0}, ${y0})`); // Punto en la función
                ggbAPI.evalCommand(`SetPointSize(${pointNameX0}, 5)`); // Tamaño del punto
                ggbAPI.evalCommand(`SetColor(${pointNameX0}, 255, 0, 0)`); // Rojo
                ggbAPI.evalCommand(`SetLabelMode(${pointNameX0}, 0)`); // Ocultar nombre

                // Poner el punto X0 nuevo sobre el eje Y
                const pointNameX0Nuevo = `PuntoX0Nuevo_${index}`;
                ggbAPI.evalCommand(`${pointNameX0Nuevo} = (${x0Nuevo}, 0)`); // Punto en Y=0
                ggbAPI.evalCommand(`SetPointSize(${pointNameX0Nuevo}, 5)`); // Tamaño del punto
                ggbAPI.evalCommand(`SetColor(${pointNameX0Nuevo}, 0, 0, 255)`); // Azul
                ggbAPI.evalCommand(`SetLabelMode(${pointNameX0Nuevo}, 0)`); // Ocultar nombre


                // Crear línea entre X0 y X0Nuevo (Línea infinita)
                const lineName = `LineaIteracion_${index}`;
                ggbAPI.evalCommand(`${lineName} = Line(${pointNameX0}, (${x0Nuevo}, 0))`);
                ggbAPI.evalCommand(`SetColor(${lineName}, 0, 255, 0)`); // Color verde
                ggbAPI.evalCommand(`SetLineThickness(${lineName}, 1)`); // Grosor de la línea

            });

            console.log("Puntos de iteración añadidos.");
        }
    });



    enviarButton.addEventListener('click', function () {
        const equationInput = document.getElementById('equation-input').value;

        const initialPointInput = document.getElementById('initial-point').value;
        const initialPointInput2 = document.getElementById('initial-point2').value;
        const selectedOption = document.querySelector('input[name="options"]:checked');
        const selectedValue = selectedOption ? selectedOption.value : null;


        // Validaciones
        if (!equationInput) {
            alert('Por favor, ingrese la ecuación original.');
            return;
        }
        if (!initialPointInput2) {
            alert('Por favor, ingrese el segundo punto Inicial B.');
            return;
        }
        if (!initialPointInput) {
            alert('Por favor, ingrese el punto inicial A.');
            return;
        }
        if (!selectedValue) {
            alert('Por favor, seleccione una tolerancia.');
            return;
        }
        const data = {
            punto_inicial_a: initialPointInput,
            punto_inicial_b: initialPointInput2,
            tolerancia: selectedValue,
            funcion: equationInput
        };
        console.log('Data a enviar:', data);

        fetch('http://localhost:5000/biseccion', {
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

                // Llenar la tabla de iteraciones
                const iteracionesTableBody = document.querySelector('.table tbody');
                iteracionesTableBody.innerHTML = ''; // Limpiar la tabla antes de llenarla

                // Asegúrate de que `data.Iteraciones` existe y es un array
if (Array.isArray(data.iteraciones)) {
    data.iteraciones.forEach(iteracion => {
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td>${iteracion.iteracion || '---'}</td>
            <td>${iteracion.punto_a !== undefined && !isNaN(iteracion.punto_a) ? iteracion.punto_a.toFixed(4) : '---'}</td>
            <td>${iteracion.punto_b !== undefined && !isNaN(iteracion.punto_b) ? iteracion.punto_b.toFixed(4) : '---'}</td>
            <td>${iteracion.punto_medio !== undefined && !isNaN(iteracion.punto_medio) ? iteracion.punto_medio.toFixed(4) : '---'}</td>
            <td>${iteracion.error !== undefined && iteracion.error !== '---' && !isNaN(iteracion.error) ? iteracion.error.toFixed(4) : iteracion.error || '---'}</td>
        `;
        iteracionesTableBody.appendChild(newRow);
    });
} else {
    console.error("La propiedad 'iteraciones' no está definida o no es un array.");
}

                // Llenar la tabla de resultados finales
                const resultadoTableBody = document.getElementById('resultadoTabla').querySelector('tbody');
                resultadoTableBody.innerHTML = ''; // Limpiar la tabla antes de llenarla

                // Asegúrate de que `data["Resultado Final"]` y `data["Número de iteraciones"]` existen
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