export function Header({ onFeatureClick }) {
    return (
      <div className="container">
        <header className="d-flex flex-wrap justify-content-center py-2  border-bottom">
          <a href="/" className="d-flex align-items-center mb-3 mb-md-0 me-md-auto link-body-emphasis text-decoration-none">
            <span className="fs-4">Calculadora</span>
          </a>
  
          <ul className="nav nav-pills" >
            {/* Cada botón llama a la función onFeatureClick con información específica */}
            <li className="nav-item">
              <button onClick={() => onFeatureClick('Información sobre Punto Fijo')} className="btn btn-outline-primary">
                Punto Fijo
              </button>
            </li>
            <li className="nav-item">
              <button onClick={() => onFeatureClick('Información sobre Bisección')} className="btn btn-outline-primary">
                Bisección
              </button>
            </li>
            <li className="nav-item">
              <button onClick={() => onFeatureClick('Información sobre Newton-Raphson')} className="btn btn-outline-danger">
                Newton-Raphson
              </button>
            </li>
            <li className="nav-item">
              <button onClick={() => onFeatureClick('Información sobre Secante')} className="btn btn-outline-danger">
                Secante
              </button>
            </li>
            <li className="nav-item">
              <button onClick={() => onFeatureClick('Información sobre el taller')} className="btn btn-outline-danger">
                Taller
              </button>
            </li>
          </ul>
        </header>
      </div>
    );
  }
  