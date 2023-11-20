import React from 'react';
import './App.css';
import textbox from './components/textbox';
import logo from './logo.svg';

function App() {
    return (
        <div className="App">
            <header className="App-header">
                <img src={logo} className="App-logo" alt="logo" />
            </header>
            <section className="App-center">
                Welcome to
                <code>HateHalt</code>a ml-based hatred semantic detector.
                <a>{textbox()}</a>
            </section>
            <section className="App-footer"></section>
        </div>
    );
}

export default App;
