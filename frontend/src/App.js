import React from 'react';
import './App.css';
import Textbox from './components/textbox';
import logo from './static/media/logo_3.png';

function App() {
    return (
        <div className="App">
            <header className="App-header">
                <img src={logo} className="App-logo" alt="logo" />
            </header>
            <section className="App-center">
                Welcome to
                <code>HateHalt</code>a ML-based hatred semantic detector.
                <p> It will classify the text as </p>
                <a>
                    <Textbox></Textbox>
                </a>
            </section>
            <section className="App-footer"></section>
        </div>
    );
}

export default App;
