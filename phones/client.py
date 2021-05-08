import socketio

sio = socketio.Client()

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

    print(f'Working on job id={job_id}: ')
    print(data['job'])

    time.sleep(5)

    # Once the job succeeds/fails, notify the server
    status = STATUS_SUCCEDED # or, STATUS_FAILED
    resp = requests.post(f"{SERVER_ENDPOINT}/jobs/{job_id}/update_status/", json={"device_id" : device_id, "status" : status}).json()

    print (f"Response from notifying server of job status: {status}")
    print(resp)

sio.connect("http://0.0.0.0:5000", namespaces=['/task_acknowledgement'])
sio.wait()