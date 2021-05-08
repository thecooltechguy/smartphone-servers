import requests
import time
import threading
import util

def register_device():
    url = "http://0.0.0.0:5000/devices/register/"
    # hardcode the params for now
    params = {
        "timestamp" : time.ctime(),
        "smart_plug_key": "key"
    }
    resp = requests.post(url, json = params)
    if resp.status_code != 200:
        print("Unsuccessful Request")
        return
    
    id = resp.json()['device_id']
    # store the device id locally in a file
    with open("./id.txt", "w") as f:
        f.write(str(id))

def send_heartbeat():
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
            "cpu" : 0.6,
            "battery": 0.82,
            
        }
    }
    #util.cpu_use(),
    #        "battery": util.battery_level(),
    #        "disk": util.disk_use(),
    #        "pluggedin": util.plugged_in()
    url = "http://0.0.0.0:5000/devices/{}/heartbeat/".format(id)
    resp = requests.post(url, json = params)
    if resp.status_code == 400:
        register_device()
        resp = requests.post(url, json = params)
    
    # send a heartbeat every 60 seconds
    threading.Timer(60, send_heartbeat).start()

register_device()
send_heartbeat()
