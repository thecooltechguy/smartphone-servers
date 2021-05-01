from datetime import datetime

from flask import Flask, request, jsonify, render_template

from models import Phone
import uuid

from flask_socketio import SocketIO, send, emit
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = "actualsecret"
socketio = SocketIO(app)

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



 # This function will send the task to a random phone using socketIO given a HTTP request from a user of this cluster
@app.route("/devices/addTask/", methods=['POST'])
def addTask():

    # for now it's a github link
    github_link = request.form.get('github_link')

    # if no key was added, then return false. They should provide a key for the smart plug
    if github_link is None:
        return jsonify(success=False, device_id=device_id, smart_plug_key="Please provide a github_link.")

    # get a random device_id and send it.
    device_id_list = list(datacenter_devices.keys())
    if(len(device_id_list) == 0):
        return jsonify(success=False, error="No phones registered")
    random_device_id = device_id_list[random.randint(0, len(device_id_list) - 1)]
    socketio.emit("task_submission", {'device_id': random_device_id, 'github_link': github_link})

    return jsonify(success=True)



'''
Socket IO events:
 - connect
 - disconnect
 - receive ACK from phones
'''
@socketio.on('connect')
def test_connect():
    print("Phone has connected")

@socketio.on('disconnect')
def test_disconnect():
    print('Phone has disconnected')

@socketio.on('task_acknowledgement')
def handle_phone_response(data):
    print("Phone responded with: ", data)

if __name__ == '__main__':
    # app.run(host="0.0.0.0")
    socketio.run(app, host='0.0.0.0')
