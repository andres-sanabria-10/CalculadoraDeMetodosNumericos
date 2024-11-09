// Obtener referencias a los elementos del DOM
const originalEquationInput = document.getElementById('equation-input');
const isolatedEquationInput = document.getElementById('calculator-input');
const calculatorKeys = document.querySelectorAll('.calculator-keypad'); // Cambiado a querySelectorAll

// Variable para mantener registro del input activo
let activeInput = originalEquationInput;

// Función para manejar el cambio de input activo
originalEquationInput.addEventListener('focus', () => {
    activeInput = originalEquationInput;
});

isolatedEquationInput.addEventListener('focus', () => {
    activeInput = isolatedEquationInput;
});

// Mostrar teclado seleccionado
function showKeyboard(keyboardId) {
    const keyboards = document.querySelectorAll('.calculator-keypad');
    keyboards.forEach(kb => {
        kb.style.display = 'none';
    });
    const selectedKeyboard = document.getElementById(keyboardId);
    if (selectedKeyboard) {
        selectedKeyboard.style.display = 'grid';
    }
}

// Función para manejar el clic en los botones de la calculadora
function handleCalculatorButtonClick(event) {
    const target = event.target.closest('button');



    // Asegurarse de que se hizo clic en un botón
    if (target) {
        let value = '';

        // Obtener la función desde data-funcion en lugar de alt
        const funcion = target.querySelector('img')?.getAttribute('data-funcion');

        switch (funcion) {
            case 'raiz_cuadrada': value = 'sqrt()'; break;
            case 'valor_absoluto': value = '|'; break;
            case 'exponente_cuadrado': value = '^2'; break;
            case 'base_exponente': value = '^'; break;
            case 'euler_Exponente': value = 'e^'; break;
            case 'raiz_indicar_radical': value = '(indice,Radicando)'; break;
            case 'borrar': value = ''; break;  // Agregar valor vacío para borrar
            case 'izquierda': handleMoveCursor('left'); return;  // Mover el cursor a la izquierda
            case 'derecha': handleMoveCursor('right'); return;  // Mover el cursor a la derecha

            default:
                value = target.textContent.trim();
                // Mapear símbolos especiales en texto
                switch (value) {
                    case '×': value = '*'; break;
                    case '÷': value = '/'; break;
                    case '−': value = '-'; break;
                    case 'π': value = 'pi'; break;
                    case 'e': value = 'e'; break;
                    case 'sen': value = 'sin( )'; break;
                    case 'cos': value = 'cos( )'; break;
                    case 'tg': value = 'tan( )'; break;
                }
        }

        // Insertar el valor en la posición del cursor
        if (activeInput) {
            const start = activeInput.selectionStart;
            const end = activeInput.selectionEnd;
            const currentValue = activeInput.value;

            // Combinar el texto actual con el nuevo valor
            activeInput.value = currentValue.substring(0, start) +
                value +
                currentValue.substring(end);

            // Mover el cursor después del valor insertado
            const newPosition = start + value.length;
            activeInput.setSelectionRange(newPosition, newPosition);

            // Mantener el foco en el input
            activeInput.focus();
        }
    }
}


// Función para agregar el evento de retroceso a todos los botones
function addBackspaceEventListeners() {
    const backspaceButtons = document.querySelectorAll('button[data-funcion="borrar"]'); // Seleccionar todos los botones con data-funcion="Borrar"

    // Agregar evento de retroceso a cada botón de borrado
    backspaceButtons.forEach(button => {
        button.addEventListener('click', handleBackspace);
    });
}

// Agregar evento de clic a todos los teclados
calculatorKeys.forEach(keyboard => {
    keyboard.addEventListener('click', handleCalculatorButtonClick);
});

// Llamar a la función para agregar los eventos de retroceso
addBackspaceEventListeners();


// Cuando el usuario haga clic en el botón de espacio
const spaceButton = document.querySelector('button[data-funcion="espacio"]');
spaceButton.addEventListener('click', () => {
    if (activeInput) {
        const start = activeInput.selectionStart;
        const end = activeInput.selectionEnd;
        const currentValue = activeInput.value;

        // Insertar un espacio en la posición actual del cursor
        activeInput.value = currentValue.substring(0, start) + ' ' + currentValue.substring(end);

        // Mover el cursor después del espacio insertado
        const newPosition = start + 1;
        activeInput.setSelectionRange(newPosition, newPosition);

        // Mantener el foco en el input
        activeInput.focus();
    }
});


// Función para mover el cursor (izquierda o derecha)
function handleMoveCursor(direction) {
    if (activeInput) {
        const start = activeInput.selectionStart;
        const end = activeInput.selectionEnd;

        let newPosition;
        if (direction === 'left') {
            newPosition = start - 1 >= 0 ? start - 1 : 0;
        } else if (direction === 'right') {
            newPosition = end + 1 <= activeInput.value.length ? end + 1 : activeInput.value.length;
        }

        // Mover el cursor a la nueva posición
        activeInput.setSelectionRange(newPosition, newPosition);
        activeInput.focus();
    }
}


// Función para manejar el retroceso (borrar)
function handleBackspace() {
    if (activeInput) {
        const start = activeInput.selectionStart;
        const end = activeInput.selectionEnd;

        // Si no hay texto seleccionado, borrar el carácter anterior al cursor
        if (start === end && start > 0) {
            // Eliminar el carácter antes del cursor
            activeInput.value = activeInput.value.substring(0, start - 1) + activeInput.value.substring(end);
            // Colocar el cursor en la posición anterior
            activeInput.setSelectionRange(start - 1, start - 1);
        } else if (start !== end) { // Si hay texto seleccionado, eliminar el texto seleccionado
            activeInput.value = activeInput.value.substring(0, start) + activeInput.value.substring(end);
            // Colocar el cursor en la nueva posición después de borrar
            activeInput.setSelectionRange(start, start);
        }

        // Mantener el foco en el input
        activeInput.focus();
    }
}

// Función para agregar el evento de retroceso a todos los botones de borrar
function addBackspaceEventListeners() {
    // Selecciona los botones con el atributo data-funcion="borrar" y data-funcion="Borrar" (de imagen)
    const backspaceButtons = document.querySelectorAll('button[data-funcion="borrar"], button[data-funcion="borrarN"], button[data-funcion="Borrar"], img[data-funcion="Borrar"]');

    // Agregar evento de retroceso a cada botón de borrado
    backspaceButtons.forEach(button => {
        button.addEventListener('click', handleBackspace);
    });
}

// Llamar a la función para agregar los eventos de retroceso
addBackspaceEventListeners();






// Función para validar la entrada y formatear la ecuación
function formatEquation(input) {
    // Aquí puedes agregar lógica para validar y formatear la ecuación
    // Por ejemplo, verificar paréntesis balanceados, formato correcto, etc.
    return input;
}

// Evento para validar mientras se escribe
[originalEquationInput, isolatedEquationInput].forEach(input => {
    input.addEventListener('input', (e) => {
        e.target.value = formatEquation(e.target.value);
    });
});