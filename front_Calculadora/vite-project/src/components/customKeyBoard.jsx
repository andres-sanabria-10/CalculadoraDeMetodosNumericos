import React from 'react';
import '../assets/Calculadora.css';

export function CustomKeyboard({ onButtonClick, getData }) {
  const handleClick = async (value) => {
    if (value === 'API') {
      try {
        const data = getData(); // Obtiene los datos actuales
        console.log('Data from :', data); // Log de los datos actuales
        console.log('Sending data to API:', data); // Log de los datos enviados

        const response = await fetch('http://127.0.0.1:5000/api/punto-fijo', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
          
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log('API response:', result); // Log de la respuesta de la API
        // Aquí puedes manejar el resultado de la API como desees
      } catch (error) {
        console.error('Error details:', error);
        if (error.name === 'TypeError' && error.message === 'Failed to fetch') {
          console.error('Network error: Unable to connect to the server. Please check if the server is running and accessible.');
        } else {
          console.error('Unexpected error:', error.message);
        }
        // Aquí puedes añadir lógica para mostrar un mensaje de error al usuario
      }
    } else {
      onButtonClick(value); // Continúa con la lógica normal para otros botones
    }
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
        <button className="key" onClick={() => handleClick('x²')}> <img src="data:image/svg+xml;base64,PHN2ZyBpZD0ic3F1YXJlIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PGRlZnM+PHN0eWxlPi5jbHMtMXtmb250LXNpemU6MTJweDtmb250LWZhbWlseTpnZW9nZWJyYS1zYW5zLXNlcmlmLCBzYW5zLXNlcmlmO308L3N0eWxlPjwvZGVmcz48dGl0bGU+c3F1YXJlPC90aXRsZT48cmVjdCB4PSIxIiB5PSI2IiB3aWR0aD0iMiIgaGVpZ2h0PSIyIi8+PHJlY3QgeD0iNSIgeT0iNiIgd2lkdGg9IjIiIGhlaWdodD0iMiIvPjxyZWN0IHg9IjkiIHk9IjYiIHdpZHRoPSIyIiBoZWlnaHQ9IjIiLz48cmVjdCB4PSIxMyIgeT0iNiIgd2lkdGg9IjIiIGhlaWdodD0iMiIvPjxyZWN0IHg9IjEiIHk9IjEwIiB3aWR0aD0iMiIgaGVpZ2h0PSIyIi8+PHJlY3QgeD0iMTMiIHk9IjE4IiB3aWR0aD0iMiIgaGVpZ2h0PSIyIi8+PHJlY3QgeD0iMTMiIHk9IjE0IiB3aWR0aD0iMiIgaGVpZ2h0PSIyIi8+PHJlY3QgeD0iMTMiIHk9IjEwIiB3aWR0aD0iMiIgaGVpZ2h0PSIyIi8+PHJlY3QgeD0iMSIgeT0iMTQiIHdpZHRoPSIyIiBoZWlnaHQ9IjIiLz48cmVjdCB4PSIxIiB5PSIxOCIgd2lkdGg9IjIiIGhlaWdodD0iMiIvPjxyZWN0IHg9IjUiIHk9IjE4IiB3aWR0aD0iMiIgaGVpZ2h0PSIyIi8+PHJlY3QgeD0iOSIgeT0iMTgiIHdpZHRoPSIyIiBoZWlnaHQ9IjIiLz48dGV4dCBjbGFzcz0iY2xzLTEiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDE2LjY5IDguOTQpIj4yPC90ZXh0Pjwvc3ZnPg==" width={24} height={24} alt="" /> </button>
        <button className="key" onClick={() => handleClick('y^()')}> <img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCI+PHBhdGggZD0iTTIyIDBoMnYyaC0yek0xOCAwaDJ2MmgtMnpNMTggNGgydjJoLTJ6TTIyIDRoMnYyaC0yeiIvPjxnPjxwYXRoIGQ9Ik0xIDZoMnYySDF6TTUgNmgydjJINXpNOSA2aDJ2Mkg5ek0xMyA2aDJ2MmgtMnpNMSAxMGgydjJIMXpNMTMgMThoMnYyaC0yek0xMyAxNGgydjJoLTJ6TTEzIDEwaDJ2MmgtMnpNMSAxNGgydjJIMXpNMSAxOGgydjJIMXpNNSAxOGgydjJINXpNOSAxOGgydjJIOXoiLz48L2c+PC9zdmc+" alt="" /></button>
        <button className="key" onClick={() => handleClick('√()')}> <img src="data:image/svg+xml;base64,PHN2ZyBpZD0ic3FydF9yb290IiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHRpdGxlPnNxcnQ8L3RpdGxlPjxyZWN0IHg9IjE0IiB5PSIxMCIgd2lkdGg9IjIiIGhlaWdodD0iMiIvPjxyZWN0IHg9IjE4IiB5PSIxMCIgd2lkdGg9IjIiIGhlaWdodD0iMiIvPjxyZWN0IHg9IjIyIiB5PSIxMCIgd2lkdGg9IjIiIGhlaWdodD0iMiIvPjxyZWN0IHg9IjIyIiB5PSIxNCIgd2lkdGg9IjIiIGhlaWdodD0iMiIvPjxyZWN0IHg9IjE0IiB5PSIxNCIgd2lkdGg9IjIiIGhlaWdodD0iMiIvPjxyZWN0IHg9IjE0IiB5PSIxOCIgd2lkdGg9IjIiIGhlaWdodD0iMiIvPjxyZWN0IHg9IjE4IiB5PSIxOCIgd2lkdGg9IjIiIGhlaWdodD0iMiIvPjxyZWN0IHg9IjIyIiB5PSIxOCIgd2lkdGg9IjIiIGhlaWdodD0iMiIvPjxwb2x5Z29uIHBvaW50cz0iMCAxMy41IDQgMTMuNSA2Ljc1IDE4IDEyIDUgMjQgNSAyNCA2LjUgMTMgNi41IDcuNSAyMCA2IDIwIDMgMTUgMCAxNSAwIDEzLjUiLz48L3N2Zz4=" width={24} height={24} alt="" /> </button>
        <button className="key" onClick={() => handleClick('e')}>e</button>
        <button className="key" onClick={() => handleClick('4')}>4</button>
        <button className="key" onClick={() => handleClick('5')}>5</button>
        <button className="key" onClick={() => handleClick('6')}>6</button>
        <button className="key operation" onClick={() => handleClick('+')}>+</button>
        <button className="key operation" onClick={() => handleClick('-')}>−</button>
        <button className="key" onClick={() => handleClick('<')}>&lt;</button>
        <button className="key" onClick={() => handleClick('>')}>&gt;</button>
        <button className="key" onClick={() => handleClick('[]')}><img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgZmlsbD0ibm9uZSI+PHBhdGggZmlsbD0iIzAwMCIgZmlsbC1ydWxlPSJldmVub2RkIiBkPSJNMTkgNEg1djJoMTRWNFpNNSAxMC4wMDFoMlY4SDV2Mi4wMDFabTQgMGgydi0ySDl2MlptNiAwaC0ydi0yaDJ2MlptMiAwaDJ2LTJoLTJ2MlptLTEwIDRINXYtMmgydjJabTEwIDhoMi4wMDF2LTJIMTd2MlptMi00aC0ydi0yaDJ2MlptLTItNGgydi0yaC0ydjJabS0xMCA0SDVWMTZoMnYyLjAwMVptLTIgNGgydi0ySDV2MlptNi4wMDEgMEg5di0yaDIuMDAxdjJabTEuOTk5IDBoMnYtMmgtMnYyWiIgY2xpcC1ydWxlPSJldmVub2RkIi8+PC9zdmc+" alt="" /></button>
        <button className="key" onClick={() => handleClick('{}')}> <img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgZmlsbD0ibm9uZSI+PGcgZmlsbD0iIzI1MjUyNSIgPjxwYXRoIGQ9Ik0xMyAyaDIuMDAxVi0uMDAxSDEzVjJabTQgMGgyVi0uMDAxaC0yVjJabTQgMGgyVi0uMDAxaC0yVjJabTAgNGgyVjRoLTJ2MlptLTggMGgyVjRoLTJ2MlptMCA0aDJWOGgtMnYyWm00IDBoMlY4aC0ydjJabTQgMGgyVjhoLTJ2MlptLTggNmgydi0yaC0ydjJabTQgMGgydi0yaC0ydjJabTQgMGgydi0yaC0ydjJabTAgNGgydi0yaC0ydjJabS04IDBoMnYtMmgtMnYyWm0wIDRoMi4wMDF2LTJIMTN2MlptNCAwaDJ2LTJoLTJ2MlptNCAwaDJ2LTJoLTJ2MlptLTktMTFoMTJ2LTJIMTJ2MlpNMCA5aDIuMDAxVjYuOTk5SDBWOVptNCAwaDJWNi45OTlINFY5Wm00IDBoMlY2Ljk5OUg4VjlabTAgNGgydi0ySDh2MlptLTggMGgydi0ySDB2MlptMCA0aDJ2LTJIMHYyWm00IDBoMnYtMkg0djJabTQgMGgydi0ySDh2MloiLz48L2c+PC9zdmc+" alt="" /></button>
        <button className="key" onClick={() => handleClick('1')}>1</button>
        <button className="key" onClick={() => handleClick('2')}>2</button>
        <button className="key" onClick={() => handleClick('3')}>3</button>
        <button className="key operation" onClick={() => handleClick('=')}>=</button>
        <button className="key function" onClick={() => handleClick('DEL')}> <img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCI+PHBhdGggZmlsbD0ibm9uZSIgZD0iTTAgMGgyNHYyNEgwVjB6Ii8+PHBhdGggZD0iTTIyIDNIN2MtLjY5IDAtMS4yMy4zNS0xLjU5Ljg4TDAgMTJsNS40MSA4LjExYy4zNi41My45Ljg5IDEuNTkuODloMTVjMS4xIDAgMi0uOSAyLTJWNWMwLTEuMS0uOS0yLTItMnptMCAxNkg3LjA3TDIuNCAxMmw0LjY2LTdIMjJ2MTR6bS0xMS41OS0yTDE0IDEzLjQxIDE3LjU5IDE3IDE5IDE1LjU5IDE1LjQxIDEyIDE5IDguNDEgMTcuNTkgNyAxNCAxMC41OSAxMC40MSA3IDkgOC40MSAxMi41OSAxMiA5IDE1LjU5eiIvPjwvc3ZnPg==" alt="" /> </button>
        <button className="key" onClick={() => handleClick('(')}>(</button>
        <button className="key" onClick={() => handleClick(')')}>)</button>
        <button className="key" onClick={() => handleClick('[:]')}> <img src="data:image/svg+xml;base64,PHN2ZyBpZD0iYWJzIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHRpdGxlPmFiczwvdGl0bGU+PHJlY3QgeD0iNSIgeT0iNSIgd2lkdGg9IjIiIGhlaWdodD0iMiIvPjxyZWN0IHg9IjkiIHk9IjUiIHdpZHRoPSIyIiBoZWlnaHQ9IjIiLz48cmVjdCB4PSIxMyIgeT0iNSIgd2lkdGg9IjIiIGhlaWdodD0iMiIvPjxyZWN0IHg9IjE3IiB5PSI1IiB3aWR0aD0iMiIgaGVpZ2h0PSIyIi8+PHJlY3QgeD0iNSIgeT0iOSIgd2lkdGg9IjIiIGhlaWdodD0iMiIvPjxyZWN0IHg9IjE3IiB5PSIxNyIgd2lkdGg9IjIiIGhlaWdodD0iMiIvPjxyZWN0IHg9IjE3IiB5PSIxMyIgd2lkdGg9IjIiIGhlaWdodD0iMiIvPjxyZWN0IHg9IjE3IiB5PSI5IiB3aWR0aD0iMiIgaGVpZ2h0PSIyIi8+PHJlY3QgeD0iNSIgeT0iMTMiIHdpZHRoPSIyIiBoZWlnaHQ9IjIiLz48cmVjdCB4PSI1IiB5PSIxNyIgd2lkdGg9IjIiIGhlaWdodD0iMiIvPjxyZWN0IHg9IjkiIHk9IjE3IiB3aWR0aD0iMiIgaGVpZ2h0PSIyIi8+PHJlY3QgeD0iMTMiIHk9IjE3IiB3aWR0aD0iMiIgaGVpZ2h0PSIyIi8+PHJlY3QgeT0iMyIgd2lkdGg9IjIiIGhlaWdodD0iMTgiLz48cmVjdCB4PSIyMiIgeT0iMyIgd2lkdGg9IjIiIGhlaWdodD0iMTgiLz48L3N2Zz4=" width={24} height={24} alt="" /> </button>
        <button className="key" onClick={() => handleClick(',')}>,</button>
        <button className="key" onClick={() => handleClick('0')}>0</button>
        <button className="key" onClick={() => handleClick('.')}>.</button>
        <button className="key function" onClick={() => handleClick('<')}> <img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCI+PHBhdGggZmlsbD0ibm9uZSIgZD0iTTAgMGgyNHYyNEgwVjB6Ii8+PHBhdGggZD0iTTE1LjQxIDE2LjU5IDEwLjgzIDEybDQuNTgtNC41OUwxNCA2bC02IDYgNiA2IDEuNDEtMS40MXoiLz48L3N2Zz4=" alt="ohh ! no aparecio" /> </button>
        <button className="key function" onClick={() => handleClick('>')}> <img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCI+PHBhdGggZmlsbD0ibm9uZSIgZD0iTTAgMGgyNHYyNEgwVjB6Ii8+PHBhdGggZD0iTTguNTkgMTYuNTkgMTMuMTcgMTIgOC41OSA3LjQxIDEwIDZsNiA2LTYgNi0xLjQxLTEuNDF6Ii8+PC9zdmc+" alt="" /> </button>
        <button className="key function" onClick={() => handleClick('API')} > <img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCI+PHBhdGggZmlsbD0ibm9uZSIgZD0iTTAgMGgyNHYyNEgwVjB6Ii8+PHBhdGggZD0iTTE5IDd2NEg1LjgzbDMuNTgtMy41OUw4IDZsLTYgNiA2IDYgMS40MS0xLjQxTDUuODMgMTNIMjFWN2gtMnoiLz48L3N2Zz4=" alt="" /> </button>
      </div>
    </div>
  );
}
