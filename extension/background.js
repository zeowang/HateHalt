// Copyright 2017 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// When you specify "type": "module" in the manifest background,
// you can include the service worker as an ES Module,

// Add a listener to create the initial context menu items,
// context menu items only need to be created at runtime.onInstalled
chrome.runtime.onInstalled.addListener(async () => {
  chrome.contextMenus.create({
    id: "selection",
    title: "Scan hate speech",
    type: "normal",
    contexts: ["selection"],
  });
});

const texts = new Set();

export function getTexts() {
  return texts;
}

chrome.contextMenus.onClicked.addListener(async (item) => {
  console.log("Clicked context menu");
  // get text
  let text = item.selectionText;
  // do something with the text
  console.log('Selected text: "' + text + '"');
  texts.add(text);

  fetch_label(text);
  // Save the updated set to chrome.storage.sync
  chrome.storage.sync.set({ texts: Array.from(texts) }, () => {
    console.log("Texts saved to storage:", Array.from(texts));
  });
});

// function that query backend given the string
const fetch_label = async (string) => {
  const json_data = {
    strings: [string],
  };

  // post request
  const response = await fetch("http://localhost:5000/api/detect", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(json_data),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! Status: ${response.status}`);
  }

  const data = await response.json();
  // Do something with the response data
  console.log("Response:", data);

  return data;
};
