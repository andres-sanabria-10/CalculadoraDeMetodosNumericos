import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [message, setMessage] = useState('') // Nuevo estado para el mensaje del backend

  // Este useEffect hará la solicitud al backend cuando el componente cargue
  useEffect(() => {
    fetch('http://localhost:5000/')  // Aquí llamas al backend Flask
      .then(response => response.json())
      .then(data => setMessage(data.message))  // Guarda el mensaje recibido en el estado
      .catch(error => console.error('Error fetching message:', error))
  }, [])

  return (
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>

      {/* Aquí agregamos el mensaje recibido del backend */}
      <div className="card">
        <h2>Mensaje desde el backend:</h2>
        <p>{message ? message : 'Cargando...'}</p> {/* Muestra el mensaje o un texto de carga */}
      </div>
    </>
  )
}

export default App
