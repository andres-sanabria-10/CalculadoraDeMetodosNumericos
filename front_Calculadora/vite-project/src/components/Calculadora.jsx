import React, { useState, useEffect, useRef } from 'react';
import '../assets/Calculadora.css';
import { CustomKeyboard } from '../components/customKeyBoard';
import { LeftContainer } from './LeftContainer';  // Importa el componente

export function Calculator({ onButtonClick }) {
  const [input, setInput] = useState('');
  const [cursorPosition, setCursorPosition] = useState(0);
  const [activeInput, setActiveInput] = useState('');  // Nuevo estado para el input activo

  const [funcionInicial, setFuncionInicial] = useState('');
  const [funcionDespejada, setFuncionDespejada] = useState('');
  const [puntoInicial, setPuntoInicial] = useState('');
  const [maxIteraciones, setMaxIteraciones] = useState('100');
  const [tolerancia, setTolerancia] = useState(''); // Add this line
  const inputRef = useRef(null);


  // Función para obtener los datos actuales
  const getData = () => {
    if (!funcionInicial || !funcionDespejada || !puntoInicial || !tolerancia || !maxIteraciones) {
      alert("Por favor, completa todos los campos");
      return;
    }
    const data = {
      Punto_inicial: puntoInicial,
      funcion: funcionInicial,
      funcion_despejada: funcionDespejada,
      max_iteraciones: maxIteraciones,
      error_percentual: selectedOption
    };
    console.log("Los datos son:", data);
    return data;
  };

  const handleClick = (value) => {
    if (activeInput === 'calculator') {
      // Lógica de calculadora
      if (value === 'DEL') {
        if (cursorPosition > 0) {
          setInput(prevInput => prevInput.slice(0, cursorPosition - 1) + prevInput.slice(cursorPosition));
          setCursorPosition(prev => prev - 1);
        }
      } else if (value === '=') {
        try {
          setInput(eval(input).toString());
          setCursorPosition(eval(input).toString().length);
        } catch (error) {
          setInput('Error');
          setCursorPosition(5);
        }
      } else if (value === '<') {
        setCursorPosition(prev => Math.max(0, prev - 1));
      } else if (value === '>') {
        setCursorPosition(prev => Math.min(input.length, prev + 1));
      } else {
        setInput(prevInput => prevInput.slice(0, cursorPosition) + value + prevInput.slice(cursorPosition));
        setCursorPosition(prev => prev + value.length);
      }
    } else if (activeInput === 'funcionDespejada') {
      setFuncionDespejada(prev => prev + value);
    } else if (activeInput === 'puntoInicial') {
      setPuntoInicial(prev => prev + value);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      handleClick('=');
    } else if (event.key === 'Backspace') {
      event.preventDefault();
      handleClick('DEL');
    } else if (event.key === 'ArrowLeft') {
      event.preventDefault();
      handleClick('<');
    } else if (event.key === 'ArrowRight') {
      event.preventDefault();
      handleClick('>');
    } else if (/^[0-9a-z+\-*/.()=,<>[\]{}]$/.test(event.key.toLowerCase())) {
      event.preventDefault();
      handleClick(event.key);
    }
  };

  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.setSelectionRange(cursorPosition, cursorPosition);
      inputRef.current.focus();
    }
  }, [cursorPosition]);

  const handleInputChange = (e) => {
    setInput(e.target.value);
    setFuncionInicial(e.target.value);
    //setCursorPosition(e.target.selectionStart);
  };

  const handleInputClick = (e) => {
    setCursorPosition(e.target.selectionStart);
  };

  // Función para manejar cuando un input de LeftContainer está enfocado
  const handleInputFocus = (inputName) => {
    setActiveInput(inputName);
  };

  return (

    <div className="layout">
      <LeftContainer

        content="Contenido de LeftContainer"
        activeInput={activeInput}
        onInputFocus={setActiveInput}
        funcionDespejada={funcionDespejada}
        setFuncionDespejada={setFuncionDespejada}
        puntoInicial={puntoInicial}
        setPuntoInicial={setPuntoInicial}
        maxIteraciones={maxIteraciones}
        setMaxIteraciones={setMaxIteraciones}
        tolerancia={tolerancia} // Add this line
        setTolerancia={setTolerancia} // Add this line

      />



      <div className="calculator-container">

        <div className="graph-area">
          {/* Área para futuros gráficos */}
        </div>
        <div className="Data">
          <div className="input-container">
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={handleInputChange}
              onClick={handleInputClick}
              style={{ caretColor: 'black' }}
              onFocus={() => handleInputFocus('calculator')}
            />
            <div
              className="cursor-indicator"
              style={{
                left: `${cursorPosition * 8}px`,
                animation: 'blink 1s step-end infinite'
              }}
            />
          </div>
        </div>

        <div className="calculator">
          <CustomKeyboard onButtonClick={handleClick} getData={getData} />
        </div>

        {/* Pasamos el handleClick y handleInputFocus a LeftContainer */}

      </div>
    </div>
  );
}