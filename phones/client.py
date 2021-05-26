import socketio
import time
import requests
import os

SERVER_ENDPOINT = "http://localhost:5000"
STATUS_FAILED = 2
STATUS_SUCCEDED = 3

# get the device id
# Note: device id 0 is registered for testing, real devices should use ids >= 1
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

    print('Working on job id={}: '.format(job_id))
    print(data['job'])

    # process the task from git repo
    process_git_task(data['job']['code_url'])

    result = ""
    with open("./output", "r") as f:
        result += f.readline()
    
    time.sleep(5)

    status = 0
    with open("./status", "r") as f:
        status = int(f.readline())

    # Once the job succeeds/fails, notify the server
    status = STATUS_SUCCEDED if status == 0 else STATUS_FAILED
    
    resp = requests.post("{}/jobs/{}/update_status/".format(SERVER_ENDPOINT, job_id), json={"device_id" : device_id, "status" : status, "result" : result}).json()

    print("Response from notifying server of job status: {}".format(status))
    print(resp)

def process_git_task(url):
    # clone the git repo
    os.system('git clone {}'.format(url))
    # get the directory
    directory = url.split('/')[-1].replace('.git', '')
    # run the file and store in a file
    os.system('./{}/main.sh > ./output'.format(directory))
    # check the exit code and store in a file
    os.system('echo $? > ./status')
    # remove the git repo
    os.system('rm -rf {}'.format(directory))

sio.connect('http://127.0.0.1:5000/?device_id={}'.format(device_id))
sio.wait()