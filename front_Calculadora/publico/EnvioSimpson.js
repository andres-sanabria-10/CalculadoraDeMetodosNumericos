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
                    width: 600,
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
            funcion: equationInput,
        };

        fetch('http://localhost:5504/simpson', {
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
                alert(data.convergencia);

                const resultadoTableBody = document.getElementById('resultadoTabla').querySelector('tbody');
                resultadoTableBody.innerHTML = '';
                const resultadoRow = document.createElement('tr');
                resultadoRow.innerHTML = `
                    <td>${typeof data.area_bajo_la_curva === 'number' ? data.area_bajo_la_curva.toFixed(4) : '---'}</td>
                    <td>${data.convergencia}</td>
                    <td>${typeof data.error_relativo === 'number' ? data.error_relativo.toFixed(4) : '---'}</td>
                    <td>${Array.isArray(data.puntos) ? data.puntos.map(p => typeof p === 'number' ? p.toFixed(4) : '---').join('<br> ') : '---'}</td>
                    <td>${Array.isArray(data.puntos_medios) ? data.puntos_medios.map(p => typeof p === 'number' ? p.toFixed(4) : '---').join('<br> ') : '---'}</td>
                    <td>${Array.isArray(data.imagenes_puntos_medios) ? data.imagenes_puntos_medios.map(p => typeof p === 'number' ? p.toFixed(4) : '---').join('<br> ') : '---'}</td>
                    <td>
                        ${Array.isArray(data.funcion_evaluada_en_puntos) && data.funcion_evaluada_en_puntos.length > 0
                        ? data.funcion_evaluada_en_puntos.map(tuple => {
                            const num = Number(tuple[0]);  // Accedemos al primer valor de la tupla
                            return !isNaN(num)
                                ? num.toFixed(4)  // Redondeamos el número a 4 decimales
                                : '---';  // Si no es un número, mostramos '---'
                        }).join('<br> ')
                        : '---'  // Si no es un array o está vacío, mostramos '---'
                    }
                    </td>
                `;
                resultadoTableBody.appendChild(resultadoRow);

                // Abrir el modal automáticamente después de agregar los resultados
                const myModal = new bootstrap.Modal(document.getElementById('resultadoModal'));
                myModal.show();

            })
            .catch(error => {
                console.error('Error:', error);
                alert(`Error al enviar los datos: ${error.message}`);
            });
    });

});
