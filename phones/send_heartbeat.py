import requests
import time
import threading
import subprocess

def register_device():
    url = "http://0.0.0.0:5000/devices/register/"
    # hardcode the params for now
    params = {
        "timestamp" : time.ctime()
    }
    resp = requests.post(url, json = params)
    if resp.status_code != 200:
        print("Unsuccessful Request")
    
    id = resp.json()['device_id']
    # store the device id locally in a file
    with open("./id.txt", "w") as f:
        f.write(id)

def send_heartbeat():
    print("Sending heartbeat")
    # get the device id
    id = None
    with open("./id.txt", "r") as f:
        id = f.readline()
    
    '''
    result = subprocess.Popen(["upower"], stdout = subprocess.PIPE)
    output = (result.communicate())
    '''
    # hardcode the params for now
    params = {
        "timestamp" : time.ctime(),
        "system" : {
            "cpu" : 0.8,
            "memory" : 16 
        }
    }
    url = "http://0.0.0.0:5000/devices/{}/heartbeat/".format(id)
    resp = requests.post(url, json = params)
    if resp.status_code == 400:
        register_device()
        resp = requests.post(url, json = params)
    
    print(resp.status_code)

    # send a heartbeat every 60 seconds
    threading.Timer(60, send_heartbeat).start()

register_device()
send_heartbeat()
