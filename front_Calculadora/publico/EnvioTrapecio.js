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
                    width: 450,
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

        fetch('http://localhost:5503/trapecio', {
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
                    <td>${data.area_bajo_la_curva}</td>
                    <td>${data.convergencia}</td>
                    <td>${data.error_relativo}</td>
                `;
                resultadoTableBody.appendChild(resultadoRow);


            })
            .catch(error => {
                console.error('Error:', error);
                alert(`Error al enviar los datos: ${error.message}`);
            });
    });

});
