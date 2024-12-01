document.addEventListener("DOMContentLoaded", function () {
    const enviarButton = document.querySelector('.key img[data-funcion="enviar"]').parentElement;


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
