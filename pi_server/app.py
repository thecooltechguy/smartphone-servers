from datetime import datetime

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, send, emit

import db
import job_checker

app = Flask(__name__)
app.config['SECRET_KEY'] = "actualsecret"
socketio = SocketIO(app)
job_checker = job_checker.JobChecker()

# TODO: Flesh out all API code to properly format and return errors as json responses
@app.route('/devices/register/', methods=['POST'])
def register_device():
    metadata = request.get_json()
    smart_plug_key = metadata.pop("smart_plug_key")
    if not smart_plug_key:
        return jsonify(success=False, error_code="MISSING_DEVICE_SMART_PLUG_KEY"), 400

    device_id = db.create_device(smart_plug_key=smart_plug_key, metadata=metadata)
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

    # TODO: need to add charging logic based on phone's battery level on heartbeat
    # possibly something like phone.metadata.charge < 20 -> phone.start_charging() ...
    if device.needs_to_start_charging():
        device.start_charging()
    elif device.needs_to_stop_charging():
        device.stop_charging()

    return jsonify(success=True)

@app.route("/devices/")
def devices_list():
    return jsonify(success=True, devices=[device.to_json() for device in db.get_all_devices()])

@app.route("/jobs/")
def jobs_list():
    return jsonify(success=True, jobs=[job.to_json() for job in db.get_all_jobs()])

@app.route("/jobs/submit/", methods=['POST'])
def job_submit():
    body = request.get_json()
    assert "resource_requirements" in body
    assert "code_url" in body

    job = db.create_job(job_spec=body)

    # Choose a device to send this job to
    # TODO: Add some sort of cron/redundancy to attempt to re-assign jobs that don't get acknowledged, etc.
    #  This should occur as some sort of cron process, but for the sake of an MVP, we just try to assign each job once

    # Choose a device id that currently doesn't have any assigned jobs
    # TODO: This logic would of course change once we begin to account for cpus/mem, at which point,
    #  the device selection query would select all devices that have enough resources to run this job, etc.
    devices_not_in_use = db.get_devices_not_currently_in_use()
    if not devices_not_in_use:
        return jsonify(success=False, error_code="ALL_DEVICES_ARE_BUSY"), 500

    # pick a device id that has the least number of failure acks and failure jobs
    min_failed_count = 100000000 # some randomly big number for now
    for device in devices_not_in_use:
        if device.num_failed_acks + device.num_failed_jobs < min_failed_count:
            target_device_id = device.id
            min_failed_count = device.num_failed_acks + device.num_failed_jobs
    
    print("[JOB ASSIGNMENT] Job", job.id, "to device", target_device_id)
    socketio.emit("task_submission", {'device_id': target_device_id, 'job': job.to_json()})

    # used to make sure that the phone eventually acknowledges it, if not then we reschedule the job
    job_checker.add_pending_acknowledgement(job.id, target_device_id)

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
        return jsonify(success=False, error_code="INVALID_DEVICE_ID"), 400

    job = db.get_job(job_id)
    if not job:
        return jsonify(success=False, error_code="INVALID_JOB_ID"), 400

    if not job.assigned_device:
        return jsonify(success=False, error_code="CANNOT_UPDATE_UNASSIGNED_JOB")

    if job.assigned_device.id != device_id:
        return jsonify(success=False, error_code="JOB_ASSIGNED_TO_ANOTHER_DEVICE"), 400

    job.status = status

    if status == db.Job.SUCCEEDED or status == db.Job.FAILED:
        # This job has finished, so it's no longer assigned to a device
        job.assigned_device = None

    job.save()
    return jsonify(success=True)

@app.before_request
def before_request():
    db.db.connect(reuse_if_open=True)

@app.after_request
def after_request(response):
    db.db.close()
    return response

'''
Socket IO events:
 - connect
 - disconnect
 - receive ACK from phones
'''
@socketio.on('connect')
def test_connect():
    device_id = request.args.get("device_id")
    device = db.get_device(device_id=device_id)
    if not device:
        # Unknown device tried to connect
        return False
    print(f"Device id={device_id} has connected")

@socketio.on('disconnect')
def test_disconnect():
    print('A device has disconnected')

@socketio.on('task_acknowledgement')
def handle_phone_response(data):
    device_id = data['device_id']
    job_id = data['job_id']

    job = db.get_job(job_id=job_id)
    job.status = db.Job.ASSIGNED
    job.assigned_device = device_id
    job.save()

    print (f"Device id={device_id} has acknowledged job id={job_id}")

if __name__ == '__main__':
    # app.run(host="0.0.0.0")
    job_checker.run()
    socketio.run(app, host='0.0.0.0')