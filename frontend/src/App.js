import React from 'react';
import './App.css';
import textbox from './components/textbox';
import logo from './logo.svg';

function App() {
    return (
        <div className="App">
            <header className="App-header">
                <img src={logo} className="App-logo" alt="logo" />
                <p>
                    Welcome to <code>HateHalt</code>, a react-based hatred semantic detector.
                </p>
                <a>
                    {textbox()}
                </a>
            </header>
        </div>
    );
}

export default App;
