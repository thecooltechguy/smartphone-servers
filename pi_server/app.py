from datetime import datetime

from flask import Flask, request, jsonify

from pi_server import db

app = Flask(__name__)

@app.route('/devices/register/', methods=['POST'])
def register_device():
    metadata = request.get_json()
    device_id = db.create_device(metadata=metadata)
    return jsonify(success=True, device_id=device_id)


@app.route("/devices/<device_id>/heartbeat/", methods=['POST'])
def device_heartbeat(device_id):
    device = db.get_device(device_id=device_id)
    if not device:
        return jsonify(success=False), 400

    # metadata stores a json object of arbitrary device related data (such as battery life, cpu mem, etc.)
    device.metadata = request.get_json()
    device.last_heartbeat = datetime.utcnow()

    device.save()
    return jsonify(success=True)

@app.route("/devices/")
def devices_list():
    return jsonify(success=True, devices=[device.to_json() for device in db.get_all_devices()])

@app.route("/jobs/submit/", methods=['POST'])
def job_submit():
    body = request.get_json()
    assert "resource_requirements" in body
    assert "code_url" in body

    job = db.create_job(job_spec=body)
    return jsonify(success=True, job_id=job.id)

@app.route("/jobs/<job_id>/update_status/", methods=['POST'])
def job_update_status(job_id):
    body = request.get_json()

    assert "device_id" in body
    assert "status" in body

    device_id = body['device_id']
    status = body['status']

    device = db.get_device(device_id)
    if not device:
        return jsonify(success=False), 400

    job = db.get_job(job_id)
    if not job:
        return jsonify(success=False), 400

    if status == "ack" and job.status != db.Job.UNASSIGNED:
        return jsonify(success=False, error_code="JOB_NOT_UNASSIGNED")

    if job.assigned_device and job.assigned_device.id != device_id:
        return jsonify(success=False, error_code="JOB_ASSIGNED_TO_ANOTHER_DEVICE")

    job.status = status
    job.assigned_device = device
    job.save()

    return jsonify(success=True)

@app.before_request
def before_request():
    db.db.connect()

@app.after_request
def after_request(response):
    db.db.close()
    return response

if __name__ == '__main__':
    with db.db:
        db.db.create_tables([db.Device, db.Job])
    app.run(host="0.0.0.0")
