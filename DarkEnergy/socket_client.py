'''
import socketio
import json

# standard Python
sio = socketio.Client()
sio.connect('http://localhost:3002')

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def connect_error(data):
    print("The connection failed!")

sio.emit('message-from-python', {'message':'Hello Im Python!'})



@sio.on('message-to-python')
def on_message(data):
    print("Message from server,",data['message'])

@sio.event
def disconnect():
    print("I'm disconnected!")

@sio.on('processes-to-python')
def process(data):
    
    #print("Processes", data['processes'])
    
    
    for tab_id, process in data['processes'].items():
        if process.get('type') == 'renderer' and process.get('tasks') and process['tasks'][0].get('tabId'):
            print("Process OS ID:", process.get('osProcessId'))
            title = process['tasks'][0].get('title')
            print("Process Tab Title:", title)
               
    print('****************************\n****************************\n')
    with open('data_from_socket.json', 'w') as fp:
        json.dump(data, fp)

# Wait for events
sio.wait()
'''

import socketio
import json
import threading

class BackgroundSocketIO(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sio = socketio.Client()

    def run(self):
        self.sio.connect('http://localhost:3002')

        @self.sio.event
        def connect():
            print("I'm connected!")

        @self.sio.event
        def connect_error(data):
            print("The connection failed!")


        self.sio.emit('message-from-python', {'message':'Hello Im Python!'})

        @self.sio.on('message-to-python')
        def on_message(data):
            print("Message from server:", data['message'])

        @self.sio.event
        def disconnect():
            print("I'm disconnected!")

        #Catch the processes coming from Chrome Extension and save them in a JSON file.
        @self.sio.on('processes-to-python')
        def process(data):
            for tab_id, process in data['processes'].items():
                if process.get('type') == 'renderer' and process.get('tasks') and process['tasks'][0].get('tabId'):
                    #print("Process OS ID:", process.get('osProcessId'))
                    title = process['tasks'][0].get('title')
                    #print("Process Tab Title:", title)

            print('****************************\n****************************\n')
            with open('data_from_socket.json', 'w') as fp:
                json.dump(data, fp)

        # Wait for events
        self.sio.wait()


