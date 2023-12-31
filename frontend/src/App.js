import React from 'react';
import './App.css';
import Textbox from './components/textbox';
import logo from './logo.svg';
import nw from './nwPlus_Logo.svg';

function App() {
    return (
        <div className="App">
            <header className="App-header">
                <img src={logo} className="App-logo" alt="logo" />
                <img src={nw} className="topRightImage" alt="nw" />
            </header>
            <section className="App-center">
                Welcome to
                <code>HateHalt</code>a ML-based hatred semantic detector.
                <p> It will classify the text as </p>
                <a>
                    <Textbox></Textbox>
                </a>
            </section>
            <section className="App-footer">
                <p>
                    <a
                        className="github-link"
                        href="https://github.com"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        GitHub
                    </a>
                </p>
            </section>
        </div>
    );
}

export default App;
