import React from 'react';
import '../assets/Calculadora.css';

export function Calculator() {
    return (
      <div className="calculator-container">
        <div className="graph-area">
          {/* Aquí iría el componente del área de gráficos */}
        </div>
        <div className="calculator">
          <div className="calculator-row">
            <button className="key function purple">123</button>
            <button className="key function">f(x)</button>
            <button className="key function">ABC</button>
            <button className="key function">#&</button>
            <button className="key function">...</button>
          </div>
          <div className="calculator-keypad">
            <button className="key">x</button>
            <button className="key">y</button>
            <button className="key">z</button>
            <button className="key">π</button>
            <button className="key">7</button>
            <button className="key">8</button>
            <button className="key">9</button>
            <button className="key operation">×</button>
            <button className="key operation">÷</button>
            <button className="key">x²</button>
            <button className="key">y^</button>
            <button className="key">√</button>
            <button className="key">e</button>
            <button className="key">4</button>
            <button className="key">5</button>
            <button className="key">6</button>
            <button className="key operation">+</button>
            <button className="key operation">−</button>
            <button className="key">&lt;</button>
            <button className="key">&gt;</button>
            <button className="key">[ ]</button>
            <button className="key">{ '{' } { '}' }</button>
            <button className="key">1</button>
            <button className="key">2</button>
            <button className="key">3</button>
            <button className="key operation">=</button>
            <button className="key function">DEL</button>
            <button className="key">(</button>
            <button className="key">)</button>
            <button className="key">[:]</button>
            <button className="key">,</button>
            <button className="key">0</button>
            <button className="key">.</button>
            <button className="key function">&lt;</button>
            <button className="key function">&gt;</button>
            <button className="key function">↵</button>
          </div>
        </div>
      </div>
    );
  }