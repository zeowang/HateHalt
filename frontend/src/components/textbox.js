import React, { useState } from 'react';
import sendRequest from './request.js';

const textbox = () => {
    const [inputValue, setInputValue] = useState('');
    const [result, setResult] = useState(null);

    const change = (event) => {
        setInputValue(event.target.value);
    };

    const click = () => {
        sendRequest(inputValue)
            .then((result) => {
                setResult(result);
            })
            .catch((err) => {
                setResult(err.message);
            });
    };

    return (
        <div>
            <input type="text" value={inputValue} onChange={change} />
            <button onClick={click}>click here</button>
            {result && (
                <div>
                    <p> Input Value: {result}</p>
                </div>
            )}
        </div>
    );
};

export default textbox;
