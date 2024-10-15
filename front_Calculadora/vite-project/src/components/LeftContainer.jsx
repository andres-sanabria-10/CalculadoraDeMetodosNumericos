import React, { useEffect } from 'react';

export function LeftContainer({
  content,
  onInputFocus,
  activeInput,
  funcionDespejada,
  setFuncionDespejada,
  puntoInicial,
  setPuntoInicial,
  tolerancia,
  setTolerancia,
}) {

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

      {/* Radio buttons para la selección de tolerancia */}
      <div>
        <label>
          <input
            type="radio"
            name="options"
            value={Math.pow(10, 1)}
            checked={tolerancia === String(Math.pow(10, 1))}
            onChange={(e) => setTolerancia(e.target.value)}
          />
          10^1
        </label>
      </div>
      <div>
        <label>
          <input
            type="radio"
            name="options"
            value={Math.pow(10, 2)}
            checked={tolerancia === String(Math.pow(10, 2))}
            onChange={(e) => setTolerancia(e.target.value)}
          />
          10^2
        </label>
      </div>
      <div>
        <label>
          <input
            type="radio"
            name="options"
            value={Math.pow(10, 3)}
            checked={tolerancia === String(Math.pow(10, 3))}
            onChange={(e) => setTolerancia(e.target.value)}
          />
          10^3
        </label>
      </div>
      <div>
        <label>
          <input
            type="radio"
            name="options"
            value={Math.pow(10, 4)}
            checked={tolerancia === String(Math.pow(10, 4))}
            onChange={(e) => setTolerancia(e.target.value)}
          />
          10^4
        </label>
      </div>
      <div>
        <label>
          <input
            type="radio"
            name="options"
            value={Math.pow(10, 5)}
            checked={tolerancia === String(Math.pow(10, 5))}
            onChange={(e) => setTolerancia(e.target.value)}
          />
          10^5
        </label>
      </div>
      <div>
        <label>
          <input
            type="radio"
            name="options"
            value={Math.pow(10, 6)}
            checked={tolerancia === String(Math.pow(10, 6))}
            onChange={(e) => setTolerancia(e.target.value)}
          />
          10^6
        </label>
      </div>
      <div>
        <label>
          <input
            type="radio"
            name="options"
            value={Math.pow(10, 7)}
            checked={tolerancia === String(Math.pow(10, 7))}
            onChange={(e) => setTolerancia(e.target.value)}
          />
          10^7
        </label>
      </div>
      <div>
        <label>
          <input
            type="radio"
            name="options"
            value={Math.pow(10, 8)}
            checked={tolerancia === String(Math.pow(10, 8))}
            onChange={(e) => setTolerancia(e.target.value)}
          />
          10^8
        </label>
      </div>
      <div>
        <label>
          <input
            type="radio"
            name="options"
            value={Math.pow(10, 9)}
            checked={tolerancia === String(Math.pow(10, 9))}
            onChange={(e) => setTolerancia(e.target.value)}
          />
          10^9
        </label>
      </div>
      <div>
        <label>
          <input
            type="radio"
            name="options"
            value={Math.pow(10, 10)}
            checked={tolerancia === String(Math.pow(10, 10))}
            onChange={(e) => setTolerancia(e.target.value)}
          />
          10^10
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
