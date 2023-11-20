import React, { useState } from 'react';
import sendRequest from './request.js';
import "./testbox.style.css"

const Textbox = () => {
    const [inputValue, setInputValue] = useState('');
    const [result, setResult] = useState(null);

    const change = (event) => {
        setInputValue(event.target.value);
    };

    const click = () => {
        sendRequest(inputValue)
            .then((result) => {
                setResult(result);
                setTimeout(() => {
                    setResult(null);
                    console.log('After 4.5 seconds');
                }, 4500);
            })
            .catch((err) => {
                setResult(err.message);
            });
    };

    const pressEnter = (events) => {
        if (events.key == 'Enter') {
            click();
        }
    };

    return (
        <div className='Textbox'>
            <input
                type="text"
                value={inputValue}
                onChange={change}
                onKeyDown={pressEnter}
                className='input-box'
            />
            <button onClick={click} className='input-button'>Check</button>
            {result && (
                <div>
                    <p> 
                    Reported Intention: {result.replace(/_/g, ' ')}
                    </p>
                </div>
            )}
        </div>
    );
};

export default Textbox;
