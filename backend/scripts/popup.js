import {getTexts} from './background.js';

createForm().catch(console.error)

async function createForm() {
    // add text to data storage
    const texts = getTexts();
    // await chrome.storage.sync.set({storedTexts: [...texts]});
    const storedTexts = await chrome.storage.sync.get("texts");
    let parsedTexts = "";
    for (let i = 0, len = storedTexts.size; i < len; i++) {
        parsedTexts += storedTexts[i] + "\n";
    }
    console.log("Stored texts:", parsedTexts);
    console.log(storedTexts);
}