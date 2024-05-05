const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);

// Socket connection

/* Creates new HTTP server for socket 
const { Server } = require("socket.io");
const io = new Server(server);




app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
  });


io.on('connection', (socket) => {
    console.log('a user connected');
    socket.on('disconnect', () => {
        console.log('user disconnected');
    });
  });


server.listen(3000, () => {
  console.log('listening on *:3000');
});
*/


let processes_from_chrome = {}

// Socket connection
/* Creates new HTTP server for socket */
var socketServer = require('http').createServer(app);
var io = require('socket.io')(socketServer , {
  cors: {
    "origin": "*",
    "methods": "GET,HEAD,PUT,PATCH,POST,DELETE",
    "preflightContinue": false,
    "optionsSuccessStatus": 204
  }
});

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
  });


/* Listen for socket connection on port 3002 */
socketServer.listen(3002, function(){
  console.log('Socket server listening on : 3002');
});

/* This event will emit when client connects to the socket server */
io.on('connection', function(socket){

    console.log('a user connected');

    socket.on('disconnect', () => {
      console.log('user disconnected');
    });

    // Event handler for custom event from client
    socket.on('customEvent', (data) => {
    console.log('Received data from client:', data.message);
      
    // Emit a response back to the client
    socket.emit('customEventResponse', { message: 'Hello from server' });

  });

  socket.on('message-from-python', (message) => {
    console.log('Message recieved', message.message)

    // Emit a response back to the client
    socket.emit('message-to-python', { message: 'I recieved your message Python!' });
  })

  //When client send processes
  socket.on('processes', (arg)=>{
    
    console.log("We got the processes\n")
    processes_data = arg.process
    processes_from_chrome = processes_data

    for (const [tabId, process] of Object.entries(processes_data)) {
      if (process.type === 'renderer' && process.tasks[0].tabId){
        console.log("Process OS ID: ", process.osProcessId)
        title = process.tasks && process.tasks[0] && process.tasks[0].title
        console.log("Process Tab Title: ", title)
      }
      
    }
  })  


 // Send processes to Python every 10 seconds
setInterval(() => {
  socket.emit('processes-to-python', {processes : processes_from_chrome });
}, 10000); // 10 seconds

  
});


/* Node application will be running on 3000 port */
server.listen(3000, () => {
    console.log('listening on *:3000');
  });