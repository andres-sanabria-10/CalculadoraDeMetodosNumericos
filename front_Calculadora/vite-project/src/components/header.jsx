import React, { useState, useEffect } from 'react';

export function Header({ onFeatureClick }) {
  const [metodoSeleccionado, setMetodoSeleccionado] = useState('');

  // Función para manejar la tecla 'Enter' o el click del botón
  const manejarTeclaEnter = () => {
    if (metodoSeleccionado) {
      console.log(`Enviando solicitud para ${metodoSeleccionado}`);
      // Aquí puedes realizar la llamada a la API basada en el método seleccionado
      // Ejemplo: fetch(`/api/${metodoSeleccionado}`, { method: 'POST' }) ...
    }
  };

  useEffect(() => {
    const manejarKeyDown = (event) => {
      // Verificar si se presiona la tecla Enter o una tecla específica del teclado interactivo
      if (event.key === 'Enter' || event.key === 'customKey') { // 'customKey' es un ejemplo, reemplaza con el valor de tu tecla interactiva
        manejarTeclaEnter();
      }
    };

    // Añadir el listener para la tecla 'Enter' y la tecla del teclado interactivo
    window.addEventListener('keydown', manejarKeyDown);

    // Limpiar el listener cuando el componente se desmonte
    return () => {
      window.removeEventListener('keydown', manejarKeyDown);
    };
  }, [metodoSeleccionado]);

  const manejarClicMetodo = (metodo) => {
    setMetodoSeleccionado(metodo); // Actualiza el método seleccionado
    onFeatureClick(`Información sobre ${metodo}`);
  };

  return (
    <div className="container">
      <header className="d-flex flex-wrap justify-content-center py-2 border-bottom">
        <a href="/" className="d-flex align-items-center mb-3 mb-md-0 me-md-auto link-body-emphasis text-decoration-none">
          <span className="fs-4">Calculadora</span>
        </a>

        <ul className="nav nav-pills">
          <li className="nav-item">
            <button
              onClick={() => manejarClicMetodo('punto-fijo')}
              className="btn btn-outline-primary">
              Punto Fijo
            </button>
          </li>
          <li className="nav-item">
            <button
              onClick={() => manejarClicMetodo('biseccion')}
              className="btn btn-outline-primary">
              Bisección
            </button>
          </li>
          <li className="nav-item">
            <button
              onClick={() => manejarClicMetodo('newton-raphson')}
              className="btn btn-outline-danger">
              Newton-Raphson
            </button>
          </li>
          <li className="nav-item">
            <button
              onClick={() => manejarClicMetodo('secante')}
              className="btn btn-outline-danger">
              Secante
            </button>
          </li>
          <li className="nav-item">
            <button
              onClick={() => manejarClicMetodo('taller')}
              className="btn btn-outline-danger">
              Taller
            </button>
          </li>
        </ul>
      </header>
    </div>
  );
}
