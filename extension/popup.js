// popup.js

createForm().catch(console.error);

import { getTexts } from './background.js';

async function createForm() {
    // add text to data storage
    const textsMap = getTexts();
    const storedTextsMap = await chrome.storage.sync.get(['textsMap']);
    console.log("test", storedTextsMap);
    const storedTexts = storedTextsMap.textsMap();

    if (storedTexts.texts) {
        const textsArray = Array.from(storedTexts.texts);

        let parsedTexts = "";
        for (let i = 0, len = textsArray.length; i < len; i++) {
            parsedTexts += textsArray[i] + "\n";
        }
        console.log("Stored texts:\n", parsedTexts);
        console.log(textsArray);

        // add text to list in html
        let list = document.getElementById("texts");
        for (let i = 0; i < textsArray.length; ++i) {
            let li = document.createElement('li');

            // text label
            let label = document.createElement('span')
            label.innerText = textsArray[i]
            li.appendChild(label);

            // color code
            let span = document.createElement('span')
            if (textsMap.get(textsArray[i]).labels[0] == "hate_speech") {
                span.classList.add("list-key-hate");
            }
            if (textsMap.get(textsArray[i]).labels[0] == "offensive_language") {
                span.classList.add("list-key-offensive");
            }
            if (textsMap.get(textsArray[i]).labels[0] == "neither") {
                span.classList.add("list-key-neither");
            }
            li.appendChild(span);

            // probability number
            let probability = document.createElement('span');
            let percentage = Math.round(Math.max(...textsMap.get(textsArray[i]).prob) * 100);
            probability.innerText = percentage.toString + "%";
            li.appendChild(probability);

            list.appendChild(li);
            console.log("Added " + li.innerText + " to HTML")
        }
    } else {
        console.log("No stored texts");
    }
}