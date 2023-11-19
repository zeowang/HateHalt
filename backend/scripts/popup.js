// popup.js
import { getTexts } from './background.js';

createForm().catch(console.error);

async function createForm() {
    // add text to data storage
    const texts = getTexts();
    const storedTexts = await chrome.storage.sync.get(['texts']);

    if (storedTexts.texts) {
        const textsArray = Array.from(storedTexts.texts);
        let parsedTexts = "";
        for (let i = 0, len = textsArray.length; i < len; i++) {
            parsedTexts += textsArray[i] + "\n";
        }
        console.log("Stored texts:\n", parsedTexts);
        console.log(textsArray);
    } else {
        console.log("No stored texts");
    }
}