(() => {
    console.log("I'm script.js")


/* Connects to the socket server */
var socket = io.connect('http://localhost:3002');
socket.on('connect', function() {
  console.log('Client connected');
});

socket.on('customEventResponse', (arg)=>{
    console.log("Message of server is: ", arg.message)
})

socket.emit('customEvent', { message: 'Hello from Client'})

    chrome.runtime.onMessage.addListener((obj, sender, response) => {
        //const { type, value, message, videoId } = obj;
        console.log("Message: ", obj.message)
        if (obj.type === "NEW") {
           console.log("Type is new")
           console.log("The URL of the web is:", obj.videoId)   
        }
        if (obj.type === "PROCESSES") {
            console.log("Type is new")
            //To see how many processes running.
            console.log(Object.keys(obj.processes).length)

            socket.emit('processes', {process: obj.processes})
             
         }
    });
})();

