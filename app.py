from datetime import datetime

from flask import Flask, request, jsonify

from models import Phone

app = Flask(__name__)

datacenter_devices = {}

@app.route('/devices/register/', methods=['POST'])
def register_device():
    device = request.get_json()
    datacenter_devices[device['id']] = Phone(id=device['id'])
    return jsonify(success=True)

@app.route("/devices/<device_id>/heartbeat/", methods=['POST'])
def device_heartbeat(device_id):
    if device_id not in datacenter_devices:
        return jsonify(success=False), 400

    phone = datacenter_devices[device_id]

    # metadata stores a json object of arbitrary device related data (such as battery life, cpu mem, etc.)
    phone.metadata = request.get_json()

    phone.last_heartbeat = datetime.utcnow()
    datacenter_devices[device_id] = phone
    return jsonify(success=True)

@app.route("/devices/")
def devices_list():
    return jsonify(success=True, devices=[phone.to_json() for phone in datacenter_devices.values()])

if __name__ == '__main__':
    app.run()
