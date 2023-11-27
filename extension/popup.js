// popup.js

createForm().catch(console.error);

async function createForm() {
    // add text to data storage
    await chrome.storage.sync.get("textsMap", function(data) {
        console.log("result", JSON.parse(data.textsMap));
        const textsMap = JSON.parse(data.textsMap);
        console.log("please work", textsMap)

        if (Object.keys(textsMap)) {
            const textsArray = Array.from(Object.keys(textsMap));
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
                li.classList.add("text-list")
    
                // text label
                let label = document.createElement('span')
                label.innerText = textsArray[i]
    
                // color code
                let span = document.createElement('span')
                if (textsMap[textsArray[i]].labels[0] == "hate_speech") {
                    span.classList.add("list-key-hate");
                    label.classList.add("label-hate");
                }
                if (textsMap[textsArray[i]].labels[0] == "offensive_language") {
                    span.classList.add("list-key-offensive");
                    label.classList.add("label-offensive");
                }
                if (textsMap[textsArray[i]].labels[0] == "good") {
                    span.classList.add("list-key-good");
                    label.classList.add("label-good");
                }
    
                // probability number
                let probability = document.createElement('span');
                let percentage = Math.round(Math.max(...textsMap[textsArray[i]].prob[0]) * 100);
                console.log("percentage", percentage);
                probability.innerText = percentage.toString() + "%";
                console.log("probability", probability);

                li.appendChild(label);
                li.appendChild(span);
                li.appendChild(probability);
                list.appendChild(li);
    
                console.log("Added " + li.innerText + " to HTML")
            }
        } else {
            console.log("No stored texts");
        }
    })
}