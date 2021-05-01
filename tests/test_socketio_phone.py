import socketio
import requests

sio = socketio.Client()
register_url = 'http://192.168.0.113:5000/devices/register/'
myobj = {"smart_plug_key": 'random_key'}

x = requests.post(register_url, data = myobj)
device_id = (x.json()["device_id"])
print("Response from register request:", x.text)

@sio.event
def connect():
    print('connection established')

@sio.event
def disconnect():
    print('disconnected from server')

@sio.on("task_submission")
def task_submission(data):
    # Check if this is for this deviceid
    if device_id != data['device_id']:
        return
    
    # TODO: now we've obtained the link, now do something with it
    print('Working on Github Link: ', data['github_link'])

    sio.emit('task_acknowledgement', {'device_id': device_id, 'response': 'Obtained task, now starting on it.'})

sio.connect('http://localhost:5000')
sio.wait()