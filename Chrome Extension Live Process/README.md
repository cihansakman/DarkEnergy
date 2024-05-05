# Chrome Extension Live Processes

This extension serves as a tool for transferring sub-process information from the Chrome Browser to the front end API using Sockets.

The integration of Sockets can be found in the [Socket Integration Repository](https://github.com/cihansakman/ChromeExtensionLiveProcesses/tree/master2)

Chrome Extension Live Processes provides a detailed breakdown of the most resource-intensive sub-processes by leveraging the capabilities of Chrome APIs, specifically the [process](https://developer.chrome.com/docs/extensions/reference/api/processes) and [tabs](https://developer.chrome.com/docs/extensions/reference/api/tabs) API.

The extension utilizes the tabs and processes APIs provided by Google Chrome to list the currently running Chrome Tabs. It displays their respective tab titles along with the corresponding Process IDs, offering users insights into the active processes within their Chrome browser

Please note that the accessibility of the Chrome Extension is limited due to its reliance on the processes API of Chrome. As a result, the extension is compatible only with the Google Chrome Dev edition. You can install the extension here: https://www.chromium.org/getting-involved/dev-channel

## Add Extension

Clone Repository

```
git clone https://github.zhaw.ch/sakmameh/EVA.git
cd "Chrome Extension Live Process"
```

1. Open your Chrome Dev edition.
2. Go to Extensions
3. Manage Extensions
4. Enable **Developer mode**
5. Load unpacked
6. Select your "Chrome Extension Live Processes" folder
7. Start your Process Info Extension from extensions

## Credits

The UI is highly inspired from project [Chrome Process Monitor](https://github.com/svengau/chrome-process-monitor)
