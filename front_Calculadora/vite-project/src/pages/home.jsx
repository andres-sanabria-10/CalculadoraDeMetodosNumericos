import { Header } from '../components/header';

export function Home() {
    return (
        <div className='principal'>
            <Header />
            <main>
                <h2>Bienvenido a la Página Principal</h2>
                <p>Este es el contenido principal de la página de inicio.</p>
            </main>
        </div>
    );
} 
