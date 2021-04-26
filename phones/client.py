import requests
import time
import threading
import subprocess

def register_device(url, id):
    print("Sending request to register device")
    # hardcode the params for now
    params = {
        "id" : id, 
        "timestamp" : time.ctime()
    }
    resp = requests.post(url, json = params)
    print(resp.status_code)

def send_heartbeat(url):
    print("Sending heartbeat")
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
    }}
    resp = requests.post(url, json = params)
    if resp.status_code == 400:
        # hardcode, need to change
        register_device("http://0.0.0.0:5000/devices/register/", "dev2")
        resp = requests.post(url, json = params)
    # send a heartbeat every 60 seconds
    threading.Timer(60, send_heartbeat, [url]).start()
    print(resp.status_code)


register_device("http://0.0.0.0:5000/devices/register/", "dev1")
send_heartbeat("http://0.0.0.0:5000/devices/dev2/heartbeat/")
