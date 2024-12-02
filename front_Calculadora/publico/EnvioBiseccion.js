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

        graficarFuncion(equationInput);

        if (dataGlobal && dataGlobal.iteraciones) {

            // Obtener los valores de punto_a y punto_b
            const puntoA = dataGlobal.iteraciones[0].punto_a;
            const puntoB = dataGlobal.iteraciones[0].punto_b;

            // Graficar el punto A
            const pointNameA = "PuntoA_0";
            ggbAPI.evalCommand(`${pointNameA} = (${puntoA}, 0)`);
            ggbAPI.evalCommand(`SetPointSize(${pointNameA}, 4)`);
            ggbAPI.evalCommand(`SetColor(${pointNameA}, 255, 0, 0)`);  
            ggbAPI.evalCommand(`ShowLabel(${pointNameA}, false)`); 

            // Graficar el punto B
            const pointNameB = "PuntoB_0";
            ggbAPI.evalCommand(`${pointNameB} = (${puntoB}, 0)`);  
            ggbAPI.evalCommand(`SetPointSize(${pointNameB}, 4)`);
            ggbAPI.evalCommand(`SetColor(${pointNameB}, 255, 0, 0)`); 
            ggbAPI.evalCommand(`ShowLabel(${pointNameB}, false)`); 

            // Graficar los puntos medios 
            dataGlobal.iteraciones.forEach((iteracion, index) => {
                const puntoMedio = iteracion.punto_medio;
                const pointNameMedio = `PuntoMedio_${index}`;

                // Graficar el punto medio
                ggbAPI.evalCommand(`${pointNameMedio} = (${puntoMedio}, 0)`);  
                ggbAPI.evalCommand(`SetPointSize(${pointNameMedio}, 4)`);
                ggbAPI.evalCommand(`SetColor(${pointNameMedio}, 0, 0, 255)`);  
                ggbAPI.evalCommand(`ShowLabel(${pointNameMedio}, false)`);

                console.log(`Iteración ${index}: Punto Medio (${puntoMedio})`);
            });


            console.log("Puntos añadidos");
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

                dataGlobal = data;

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