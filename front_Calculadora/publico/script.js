const calculatorKeys = document.querySelectorAll('.calculator-keypad');
let activeInput = null;

// Función para registrar todos los inputs que usarán el teclado
function registerCalculatorInputs() {
    const calculatorInputs = document.querySelectorAll('.calculator-input');
    
    calculatorInputs.forEach(input => {
        // Cambiar el tipo de input a text para permitir selección
        input.type = 'text';
        // Agregar atributos para simular comportamiento numérico
        input.inputMode = 'decimal';
        input.pattern = '[0-9]*';
        
        input.removeEventListener('focus', inputFocusHandler);
        input.addEventListener('focus', inputFocusHandler);
        
    });
}
function inputFocusHandler(event) {
    activeInput = event.target;
}
// Registrar inputs al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    registerCalculatorInputs();
});

// Llamar a la función cuando se cargue la página
document.addEventListener('DOMContentLoaded', registerCalculatorInputs);

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
    if (target && activeInput) {
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
            case 'borrar': value = ''; break;
            case 'izquierda': handleMoveCursor('left'); return;
            case 'derecha': handleMoveCursor('right'); return;

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

        try {
            // Insertar el valor en la posición del cursor
            const start = activeInput.selectionStart || 0;
            const end = activeInput.selectionEnd || 0;
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
        } catch (error) {
            console.warn('Error al manipular la selección:', error);
            // Fallback: simplemente agregar el valor al final
            activeInput.value += value;
        }
    }
}

// Función para manejar el retroceso (borrar)
function handleBackspace() {
    if (activeInput) {
        try {
            const start = activeInput.selectionStart || 0;
            const end = activeInput.selectionEnd || 0;

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
        } catch (error) {
            console.warn('Error al manipular la selección durante el borrado:', error);
            // Fallback: simplemente borrar el último carácter
            activeInput.value = activeInput.value.slice(0, -1);
        }
    }
}

// Función para agregar el evento de retroceso a todos los botones
function addBackspaceEventListeners() {
    const backspaceButtons = document.querySelectorAll('button[data-funcion="borrar"], button[data-funcion="borrarN"], button[data-funcion="Borrar"], img[data-funcion="Borrar"]');
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

// Manejar el botón de espacio
const spaceButton = document.querySelector('button[data-funcion="espacio"]');
if (spaceButton) {
    spaceButton.addEventListener('click', () => {
        if (activeInput) {
            try {
                const start = activeInput.selectionStart || 0;
                const end = activeInput.selectionEnd || 0;
                const currentValue = activeInput.value;

                // Insertar un espacio en la posición actual del cursor
                activeInput.value = currentValue.substring(0, start) + ' ' + currentValue.substring(end);

                // Mover el cursor después del espacio insertado
                const newPosition = start + 1;
                activeInput.setSelectionRange(newPosition, newPosition);

                // Mantener el foco en el input
                activeInput.focus();
            } catch (error) {
                console.warn('Error al insertar espacio:', error);
                // Fallback: agregar espacio al final
                activeInput.value += ' ';
            }
        }
    });
}

// Función para validar la entrada y formatear la ecuación
function formatEquation(input) {
    // Aquí puedes agregar lógica para validar y formatear la ecuación
    return input;
}