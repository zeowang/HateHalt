import React, { useState } from 'react';

const textbox = () => {
    const [inputValue, setInputValue] = useState('');
    const [result, setResult] = useState(null);

    const change = (event) => {
        setInputValue(event.target.value);
    };

    const click = () => {
        setResult(inputValue)
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
}

export default textbox;
