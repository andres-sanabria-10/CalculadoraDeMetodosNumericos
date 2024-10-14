import React, { useEffect,useState } from 'react';

export function LeftContainer({
  content,
  onInputFocus,
  activeInput,
  funcionDespejada,
  setFuncionDespejada,
  puntoInicial,
  setPuntoInicial

}) {
  const [selectedOption, setSelectedOption] = useState('');

  const handleOptionChange = (event) => {
    setSelectedOption(event.target.value);
  };

  const handleFuncionDespejadaFocus = () => onInputFocus('funcionDespejada');
  const handlePuntoInicialFocus = () => onInputFocus('puntoInicial');

  useEffect(() => {
    if (activeInput === 'funcionDespejada') {
      document.getElementById('funcionDespejadaInput').focus();
    } else if (activeInput === 'puntoInicial') {
      document.getElementById('puntoInicialInput').focus();
    }
  }, [activeInput]);


  return (
    <div className="left-container">
      <h3>{content}</h3>
      <p>Seleccione el error porcentual:</p>

      {/* Aquí van los radio buttons */}
      <div>
        <label>
          <input
            type="radio"
            name="options"
            value="opcion1"
            checked={selectedOption === 'opcion1'}
            onChange={handleOptionChange}
          />
          Opción 1
        </label>
      </div>
      <div>
        <label>
          <input
            type="radio"
            name="options"
            value="opcion2"
            checked={selectedOption === 'opcion2'}
            onChange={handleOptionChange}
          />
          Opción 2
        </label>
      </div>
      <div>
        <label>
          <input
            type="radio"
            name="options"
            value="opcion3"
            checked={selectedOption === 'opcion3'}
            onChange={handleOptionChange}
          />
          Opción 3
        </label>
      </div>
      <div>
        <label>
          <input
            type="radio"
            name="options"
            value="opcion4"
            checked={selectedOption === 'opcion4'}
            onChange={handleOptionChange}
          />
          Opción 4
        </label>
      </div>
      <div>
        <label>
          <input
            type="radio"
            name="options"
            value="opcion5"
            checked={selectedOption === 'opcion5'}
            onChange={handleOptionChange}
          />
          Opción 5
        </label>
      </div>
      <div>
        <label>
          <input
            type="radio"
            name="options"
            value="opcion6"
            checked={selectedOption === 'opcion6'}
            onChange={handleOptionChange}
          />
          Opción 6
        </label>
      </div>
      <div>
        <label>
          <input
            type="radio"
            name="options"
            value="opcion7"
            checked={selectedOption === 'opcion7'}
            onChange={handleOptionChange}
          />
          Opción 7
        </label>
      </div>
      <div>
        <label>
          <input
            type="radio"
            name="options"
            value="opcion8"
            checked={selectedOption === 'opcion8'}
            onChange={handleOptionChange}
          />
          Opción 8
        </label>
      </div>
      <div>
        <label>
          <input
            type="radio"
            name="options"
            value="opcion9"
            checked={selectedOption === 'opcion9'}
            onChange={handleOptionChange}
          />
          Opción 9
        </label>
      </div>
      <div>
        <label>
          <input
            type="radio"
            name="options"
            value="opcion10"
            checked={selectedOption === 'opcion10'}
            onChange={handleOptionChange}
          />
          Opción 10
        </label>
      </div>



      <div style={{ marginTop: '10px' }}>
        <h4>Función despejada</h4>
        <input
          id="funcionDespejadaInput"
          type="text"
          value={funcionDespejada}
          onChange={(e) => setFuncionDespejada(e.target.value)}
          onFocus={handleFuncionDespejadaFocus}
          placeholder="Escribe la función despejada aquí"
          style={{
            width: '100%',
            padding: '8px',
            borderRadius: '4px',
            border: '1px solid #ccc',
          }}
        />
      </div>
      <div style={{ marginTop: '10px' }}>
        <h4>Punto inicial</h4>
        <input
          id="puntoInicialInput"
          type="text"
          value={puntoInicial}
          onChange={(e) => setPuntoInicial(e.target.value)}
          onFocus={handlePuntoInicialFocus}
          placeholder="Escribe el punto inicial aquí"
          style={{
            width: '100%',
            padding: '8px',
            borderRadius: '4px',
            border: '1px solid #ccc',
          }}
        />
      </div>





    </div>
  );
}
