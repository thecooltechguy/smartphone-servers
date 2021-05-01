from datetime import datetime

from flask import Flask, request, jsonify

from models import Phone
import uuid
from socket_server import *

PORT = 2222

app = Flask(__name__)

# socket server to communicate with phones
socketServer = SocketServer(PORT)
socketServer.start()

datacenter_devices = {}

@app.route('/devices/register/', methods=['POST'])
def register_device():
    device_id = str(uuid.uuid4())
    smart_plug_key = request.form.get('smart_plug_key')

    # if no key was added, then return false. They should provide a key for the smart plug
    if smart_plug_key is None:
        return jsonify(success=False, device_id=device_id, smart_plug_key="Please provide a key for the IFTTT smart plug.")
    phone = Phone(id=device_id, key=smart_plug_key)
    phone.metadata = request.get_json()
    datacenter_devices[device_id] = phone

    return jsonify(success=True, device_id=device_id, smart_plug_key=smart_plug_key)

@app.route("/devices/<device_id>/heartbeat/", methods=['POST'])
def device_heartbeat(device_id):
    if device_id not in datacenter_devices:
        return jsonify(success=False), 400

    phone = datacenter_devices[device_id]

    # metadata stores a json object of arbitrary device related data (such as battery life, cpu mem, etc.)
    phone.metadata = request.get_json()

    phone.last_heartbeat = datetime.utcnow()
    datacenter_devices[device_id] = phone

    # TODO: need to add charging logic based on phone's battery level on heartbeat
    # possibly something like phone.metadata.charge < 20 -> phone.start_charging() ...

    return jsonify(success=True)

@app.route("/devices/")
def devices_list():
    return jsonify(success=True, devices=[phone.to_json() for phone in datacenter_devices.values()])


@app.route("/devices/<device_id>/addTask/", methods=['POST'])
def addTask(device_id):
    if device_id not in datacenter_devices:
        return jsonify(success=False), 400
    socketServer.sendTask(device_id, Task("sick.com"))

    return jsonify(success=True)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
