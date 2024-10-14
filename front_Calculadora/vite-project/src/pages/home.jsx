import { useState } from 'react';
import { Header } from '../components/header';
import { Calculator } from '../components/Calculadora';
import { RigthContainer } from '../components/RightContainer';
import { LeftContainer } from '../components/LeftContainer';
import '../assets/home_css.css';

export function Home() {
  const [infoContenedor, setInfoContenedor] = useState('Información inicial');
  const [activeInput, setActiveInput] = useState(''); // El input activo
  const [inputValue, setInputValue] = useState(''); // El valor del teclado

  const actualizarInfoContenedor = () => {
    setInfoContenedor('Información actualizada con el botón Feature');
  };

  // Función que captura la tecla presionada desde el teclado personalizado
  const handleKeyPress = (keyValue) => {
    setInputValue(prevValue => prevValue + keyValue);
  };

  // Función para manejar el input que tiene el foco en LeftContainer
  const handleInputFocus = (inputName) => {
    setActiveInput(inputName); // Actualizamos qué input tiene el foco
  };

  return (
    <div className="principal">
      <Header onFeatureClick={actualizarInfoContenedor} />

      <div className="layout">
      

        <main>
          <Calculator 
            onKeyPress={handleKeyPress} // Pasamos el evento de teclas a Calculator
            activeInput={activeInput} // También podemos pasar el input activo aquí
          />
        </main>
        
        <RigthContainer content={infoContenedor} />
      </div>
    </div>
  );
}
