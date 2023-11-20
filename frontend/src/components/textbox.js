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
            <button onClick={click}>submit</button>
            {result && (
                <div>
                    <p> Reported Intention: {result}</p>
                </div>
            )}
        </div>
    );
};

export default textbox;
