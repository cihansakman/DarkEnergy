chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  console.log("Page Updated...", tab)
    const queryParameters = tab.url.split("?")[1];
    const urlParameters = new URLSearchParams(queryParameters);

  
    chrome.tabs.sendMessage(tabId, 
      message = {
      type: "NEW",
      videoId: tab.url,
      message: "The page is reloaded"

    },
    );
});



/*
  function getCurrentTabId(callback){
    chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
          const currentTabId = tabs[0].id;
          callback(currentTabId);     
    });
  }
  
  //Get the processes information livevly using Chrome Processes API
  chrome.processes.onUpdatedWithMemory.addListener(processes => {

    getCurrentTabId(currentTabId => {
      chrome.tabs.sendMessage(currentTabId, 
        message = {
        type: "PROCESSES",
        processes: processes,
        message: "Processes recieved"
  
      },
      );
    });
      

  });
*/



function getCurrentTabId(callback) {
  chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
    const currentTabId = tabs[0].id;
    callback(currentTabId);
  });
}

function sendProcessesToContentScript(processes) {
  getCurrentTabId(currentTabId => {
    chrome.tabs.sendMessage(currentTabId, {
      type: "PROCESSES",
      processes: processes,
      message: "Processes received"
    });
  });
}


//Send the process info if isEnabled true.
//In the future, we can add a send info button to send processes if only user clicks the button.
let isEnabled = true;
let counter = 0;

chrome.processes.onUpdatedWithMemory.addListener(processes => {
  counter++;

  //Send message in every 30secs
  if (isEnabled && (counter % 30 === 0 || counter == 0)) {
    sendProcessesToContentScript(processes);
  }
});


