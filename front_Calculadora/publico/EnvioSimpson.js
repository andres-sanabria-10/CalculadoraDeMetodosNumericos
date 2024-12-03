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
                    width: 580,
                    height: 300,
                    showToolBar: false,
                    showAlgebraInput: false,
                    showMenuBar: false,
                    appletOnLoad: function () {
                        ggbAPI = window["ggbApplet"];
                        console.log("GeoGebra cargado correctamenteo .");
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
        const a = parseFloat(document.getElementById('initial-point').value);
        const b = parseFloat(document.getElementById('initial-point2').value);
        const n = parseInt(document.getElementById('initial-point3').value);
    
        if (!equationInput || isNaN(a) || isNaN(b) || isNaN(n) || n <= 0) {
            alert("Por favor, ingresa una función válida, un intervalo [a, b] y un número de subintervalos positivo.");
            return;
        }
    
        // Graficar la función original
        graficarFuncion(equationInput);
    
        // Agregar las subdivisiones del intervalo
        const step = (b - a) / n;
        const points = [];
    
        // Crear los puntos en GeoGebra y agregar las líneas
        for (let i = 0; i <= n; i++) {
            const x = a + i * step;
            const fAtX = `fAtX_${i}`;
            ggbAPI.evalCommand(`${fAtX} = ${equationInput.replace(/x/g, `(${x})`)}`);
            const functionValue = ggbAPI.getValue(fAtX);
    
            // Crear un punto en GeoGebra
            ggbAPI.evalCommand(`F_${i} = (${x}, ${functionValue})`);
            ggbAPI.evalCommand(`X_${i} = (${x}, 0)`);
    
            // Agregar los puntos F_i al arreglo de puntos
            points.push(`F_${i}`);
    
            const trapezoidalCommand = `TrapezoidalSum(${equationInput}, ${a}, ${b}, ${n})`;
            ggbAPI.evalCommand(`area = ${trapezoidalCommand}`);
        }
    
        // Graficar puntos medios y sus imágenes
        if (dataGlobal && dataGlobal.puntos_medios && dataGlobal.puntos_medios.length > 0) {
            dataGlobal.puntos_medios.forEach((puntoMedio, index) => {
                const xMedio = puntoMedio;
                const fMedio = `fAtX_${index + 100}`; // Creación de fAtX para puntos medios
                ggbAPI.evalCommand(`${fMedio} = ${equationInput.replace(/x/g, `(${xMedio})`)}`);
                const functionValueMedio = ggbAPI.getValue(fMedio);
    
                // Crear punto medio en GeoGebra
                ggbAPI.evalCommand(`Xm_${index} = (${xMedio}, 0)`); // Puntos medios en el eje X
                ggbAPI.evalCommand(`Fm_${index} = (${xMedio}, ${functionValueMedio})`); // Puntos medios en la curva
    
                // Graficar línea punteada entre el punto medio y su imagen en el eje X
                ggbAPI.evalCommand(`L${index} = Line(Xm_${index}, Fm_${index})`); // Línea entre Xm y Fm
                ggbAPI.evalCommand(`SetColor(L${index}, "red")`); // Color de la línea
                ggbAPI.evalCommand(`SetLineStyle(L${index}, 2)`); // Estilo punteado (2 = punteado)
                ggbAPI.evalCommand(`SetLineThickness(L${index}, 1)`);
    
                // Crear la imagen del punto medio
                ggbAPI.evalCommand(`(Xm_${index}, "(${xMedio}, 0)")`);
                ggbAPI.evalCommand(`(Fm_${index}, "(${xMedio}, ${functionValueMedio})")`);
    
                // Cambiar el tamaño de la fuente de las etiquetas
               // ggbAPI.evalCommand(`(Xm_${index})`); 
                //ggbAPI.evalCommand(`(Fm_${index})`); 
                // Colocar los puntos medios y sus imágenes de color rojo
                ggbAPI.evalCommand(`SetColor(Xm_${index}, "red")`); 
                ggbAPI.evalCommand(`SetColor(Fm_${index}, "red")`);
            });
        }
    
        console.log(`Líneas creadas desde ${a} hasta ${b} con ${n} subintervalos.`);
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

                dataGlobal = data;

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
