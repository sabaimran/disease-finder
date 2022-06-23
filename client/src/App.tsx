import logo from './assets/logo192.png';
import './App.css';

import { Link } from 'react-router-dom';

function App() {

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Probably Genetic Disease Finder
        </p>
        <Link className="nav-menu" to="/disorders">Disorders</Link>
        <Link className="nav-menu" to="/symptoms">Symptoms</Link>
      </header>
      <div className="footer">
        <a className="source-code" href="https://github.com/sabaimran/disease-finder">🏕️ Source Code</a>
      </div>
    </div>
  );
}

export default App;
