import React from 'react';
import '../assets/Calculadora.css';

export function CustomKeyboard({ onButtonClick }) {
    const handleClick = (value) => {
        onButtonClick(value);
      };

  return (
    <div className="custom-keyboard">
      <div className="calculator-row">
        <button className="key function purple" onClick={() => handleClick('123')}>123</button>
        <button className="key function" onClick={() => handleClick('f(x)')}>f(x)</button>
        <button className="key function" onClick={() => handleClick('ABC')}>ABC</button>
        <button className="key function" onClick={() => handleClick('#&')}>#&</button>
        <button className="key function" onClick={() => handleClick('...')}>...</button>
      </div>
      <div className="calculator-keypad">
        <button className="key" onClick={() => handleClick('x')}>x</button>
        <button className="key" onClick={() => handleClick('y')}>y</button>
        <button className="key" onClick={() => handleClick('z')}>z</button>
        <button className="key" onClick={() => handleClick('π')}>π</button>
        <button className="key" onClick={() => handleClick('7')}>7</button>
        <button className="key" onClick={() => handleClick('8')}>8</button>
        <button className="key" onClick={() => handleClick('9')}>9</button>
        <button className="key operation" onClick={() => handleClick('*')}>×</button>
        <button className="key operation" onClick={() => handleClick('/')}>÷</button>
        <button className="key" onClick={() => handleClick('x²')}>x²</button>
        <button className="key" onClick={() => handleClick('y^()')}>y^()</button>
        <button className="key" onClick={() => handleClick('√()')}>√()</button>
        <button className="key" onClick={() => handleClick('e')}>e</button>
        <button className="key" onClick={() => handleClick('4')}>4</button>
        <button className="key" onClick={() => handleClick('5')}>5</button>
        <button className="key" onClick={() => handleClick('6')}>6</button>
        <button className="key operation" onClick={() => handleClick('+')}>+</button>
        <button className="key operation" onClick={() => handleClick('-')}>−</button>
        <button className="key" onClick={() => handleClick('<')}>&lt;</button>
        <button className="key" onClick={() => handleClick('>')}>&gt;</button>
        <button className="key" onClick={() => handleClick('[]')}>[]</button>
        <button className="key" onClick={() => handleClick('{}')}>{'{}'}</button>
        <button className="key" onClick={() => handleClick('1')}>1</button>
        <button className="key" onClick={() => handleClick('2')}>2</button>
        <button className="key" onClick={() => handleClick('3')}>3</button>
        <button className="key operation" onClick={() => handleClick('=')}>=</button>
        <button className="key function" onClick={() => handleClick('DEL')}>DEL</button>
        <button className="key" onClick={() => handleClick('(')}>(</button>
        <button className="key" onClick={() => handleClick(')')}>)</button>
        <button className="key" onClick={() => handleClick(',')}>,</button>
        <button className="key" onClick={() => handleClick('0')}>0</button>
        <button className="key" onClick={() => handleClick('.')}>.</button>
      </div>
    </div>
  );
}
