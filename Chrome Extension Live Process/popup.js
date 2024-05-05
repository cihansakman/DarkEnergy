document.addEventListener('DOMContentLoaded', function() {

    //First get the current tab id using tabs API
    //Then get the corresponding process id for these tab to understand which tab is currently active
    function getCurrentTabProcessId(callback) {
      chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
        chrome.processes.getProcessIdForTab(tabs[0].id, (currentProcessId) => {
            const currentTabId = currentProcessId;
            callback(currentTabId);
          });
        
      });
    }

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


     
  

     
        
      const tabList = document.getElementById('tabList');
      tabList.innerHTML = ''; // Clear the list before updating
  
      for (const [tabId, process] of Object.entries(processes)) {
        if (process.type === 'renderer' && process.tasks[0].tabId) {
          const row = document.createElement('tr');
          const tabIdCell = document.createElement('td');
          const processIdCell = document.createElement('td');
          const taskCell = document.createElement('td');
          const cpu = document.createElement('td');
          const activeCell = document.createElement('td');
  
          tabIdCell.textContent = process.tasks[0].tabId;
          processIdCell.textContent = process.osProcessId;
          taskCell.textContent = process.tasks && process.tasks[0] && process.tasks[0].title;
          cpu.textContent = (Math.round(parseFloat(process.cpu) * 100) / 100).toFixed(2); 
  
          getCurrentTabProcessId(currentTab => {
            if (currentTab == process.id) {
              row.style.backgroundColor = '#f5d742';
              activeCell.textContent = 'Active';
            }else{
                activeCell.textContent = 'Inactive';
            }
          });
  
          row.appendChild(tabIdCell);
          row.appendChild(processIdCell);
          row.appendChild(taskCell);
          row.appendChild(cpu);
          row.appendChild(activeCell);
  
          tabList.appendChild(row);
        }
      }
    });
  });


  