import socketio
import requests
import time

SERVER_ENDPOINT = "http://localhost:5000"

sio = socketio.Client()
register_url = f'{SERVER_ENDPOINT}/devices/register/'
myobj = {"smart_plug_key": 'random_key'}

resp = requests.post(register_url, json = myobj).json()
device_id = (resp["device_id"])

print("Response from register request:")
print(resp)

STATUS_FAILED = 2
STATUS_SUCCEDED = 3

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

    job_id = data['job']['id']

    sio.emit('task_acknowledgement', {'device_id': device_id, 'job_id' : job_id})

    # TODO: now we've obtained the link, now do something with it
    print(f'Working on job id={job_id}: ')
    print(data['job'])

    # TODO: Note, without this, somehow the requests.post() call to update status reaches the server before the sio.emit(task_ack)
    #  which will cause an error because the task only gets officially assigned to this device in the db after the sio.emit call
    #  but we can just work around this by having a time.sleep() here to simulate work being done and realistically, this wont
    #  happen in real use-cases, since the time to download the code, etc. will ensure enough ample time in between the sio.emit() above
    #  and the request.post below for updating job status
    time.sleep(5)

    # Once the job succeeds/fails, notify the server
    status = STATUS_SUCCEDED # or, STATUS_FAILED
    resp = requests.post(f"{SERVER_ENDPOINT}/jobs/{job_id}/update_status/", json={"device_id" : device_id, "status" : status}).json()

    print (f"Response from notifying server of job status: {status}")
    print(resp)

sio.connect(f'http://localhost:5000/?device_id={device_id}')
sio.wait()