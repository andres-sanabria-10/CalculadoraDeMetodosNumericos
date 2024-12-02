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


            dataGlobal.iteraciones.forEach((iteracion, index) => {
                const x0 = iteracion.x0;
                const x1 = iteracion.x1;

                const puntoX0 = `PuntoX0_${index+1}`;
                const puntoX1 = `PuntoX1_${index+1}`;
                const secante = `Secante_${index+1}`;
                
                ggbAPI.evalCommand(`${puntoX0} = (${x0}, f(${x0}))`);
                ggbAPI.evalCommand(`${puntoX1} = (${x1}, f(${x1}))`);
                ggbAPI.evalCommand(`${secante} = Line(${puntoX0}, ${puntoX1})`);

                ggbAPI.setLabelVisible(puntoX0, false);
                ggbAPI.setLabelVisible(puntoX1, false);
    
                const color = colors[index % colors.length];
                ggbAPI.setLabelVisible(secante, false);
                ggbAPI.setColor(secante, ...color);
                ggbAPI.setLineThickness(secante, 2);

                // Establecer el color de los puntos 
                ggbAPI.setColor(puntoX0, ...color);
                ggbAPI.setColor(puntoX1, ...color);

                // Crear el texto de información 
                const labelName = `Label_${index+1}`; 
                const label = `I: ${index+1}`; 
                ggbAPI.evalCommand(`${labelName}=Text("${label}", (${x0}, 0))`); 
                ggbAPI.setVisible(labelName, true);
                ggbAPI.setColor(labelName,...color);

                // Agregar el evento para mostrar/ocultar la etiqueta
                ggbAPI.registerObjectUpdateListener(secante, () => {
                    const isMouseOver = ggbAPI.isObjectUnderMouse(secante);
                    console.log(`Mouse sobre ${secante}: ${isMouseOver}`);
                    ggbAPI.setVisible(labelName, isMouseOver);
                });
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
            x0: initialPointInput,
            x1: initialPointInput2,
            tolerancia: selectedValue,
            funcion: equationInput
        };
        console.log('Data a enviar:', data);

        fetch('http://localhost:5400/secante', {
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
            <td>${iteracion.x0 !== undefined && !isNaN(iteracion.x0) ? iteracion.x0.toFixed(4) : '---'}</td>
            <td>${iteracion.x1 !== undefined && !isNaN(iteracion.x1) ? iteracion.x1.toFixed(4) : '---'}</td>
            <td>${iteracion.x2 !== undefined && !isNaN(iteracion.x2) ? iteracion.x2.toFixed(4) : '---'}</td>
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