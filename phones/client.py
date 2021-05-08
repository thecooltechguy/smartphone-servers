import socketio
import time
import requests
import os

SERVER_ENDPOINT = "http://localhost:5000"
STATUS_FAILED = 2
STATUS_SUCCEDED = 3
# get the device id
device_id = None
with open("./id.txt", "r") as f:
    device_id = int(f.readline())

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

    # process the task from git repo
    # TODO: process more complicated tasks
    process_git_task(data['job']['code_url'])

    # TODO: have more logic in terms of catching and handling errors, and process results
    result = ""
    with open("./output", "r") as f:
        result += f.readline()
    
    time.sleep(5)

    # Once the job succeeds/fails, notify the server
    status = STATUS_SUCCEDED # or, STATUS_FAILED
    
    # TODO: sending the response
    resp = requests.post(f"{SERVER_ENDPOINT}/jobs/{job_id}/update_status/", json={"device_id" : device_id, "status" : status, "result" : result}).json()

    print(f"Response from notifying server of job status: {status}")
    print(resp)

def process_git_task(url):
    # clone the git repo
    os.system('git clone {}'.format(url))
    # get the directory
    directory = url.split('/')[-1].replace('.git', '')
    # run the file and store in a output file
    os.system('./{}/main.sh > ./output'.format(directory))
    # remove the git repo
    os.system('rm -rf {}'.format(directory))

sio.connect(f'http://127.0.0.1:5000/?device_id={device_id}')
sio.wait()