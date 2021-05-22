import threading
import db
import requests

from datetime import timedelta
import datetime

SERVER_ENDPOINT = "http://localhost:5000"
submit_job_url = f"{SERVER_ENDPOINT}/jobs/submit/"

# JobChecker 
# 1. checks each job to see if they time out
# 2. if job times out, restart it
# 3. if job repeatedly fails, then stop it after 3 retries
# 4. if phone does not acknowledge task, increment its failed acks num
class JobChecker:

    def __init__(self):
        self.stopped = False
        self.pending_job_acks = {}

    def check_job(self):
        while not self.stopped:
            jobs = db.get_all_jobs()

            # for each job...
            for job in jobs:
                job_json = job.to_json()
                job_max_secs = job_json["resource_requirements"]["max_runtime_secs"]

                # Check if job timed out, if so then try to cancel it and reschedule it.
                if job_max_secs > 0 and job_json["status"] == job.ASSIGNED and job_json["assigned_device_id"] is not None:
                    time_updated = datetime.datetime.strptime(job_json["time_updated"], '%Y-%m-%d %H:%M:%S.%f')
                    timeout_datetime = timedelta(seconds = job_max_secs) + time_updated
                    if timeout_datetime < datetime.datetime.utcnow():

                        # update device's num_failed_jobs
                        device = db.get_device(job_json["assigned_device_id"])
                        device.num_failed_jobs += 1
                        device.save()

                        print(device.num_failed_jobs)
                        print("Timed out job on", device.id, "on Job", job.id)

                        cancel_and_reschedule_job(job.id)

                # Check if the phone has not acknowledged the job for 10 seconds. If so, then increase the num_failed_acks and reschedule the job
                if job_json["status"] == job.UNASSIGNED:
                    time_updated = datetime.datetime.strptime(job_json["time_updated"], '%Y-%m-%d %H:%M:%S.%f')
                    timeout_datetime = timedelta(seconds = 10) + time_updated
                    if timeout_datetime < datetime.datetime.utcnow() and job.id in self.pending_job_acks:

                        # update device's num_failed_acks
                        device = db.get_device(self.pending_job_acks[job.id])
                        device.num_failed_acks += 1
                        device.save()

                        print(device.num_failed_acks)
                        print("No acknowledgement from", device.id, "on Job", job.id)

                        self.remove_pending_acknowledgement(job.id)
                        self.cancel_and_reschedule_job(job.id)


                

    def stop(self):
        self.stopped = True

    def run(self):
        t1 = threading.Thread(target=self.check_job)
        t1.start()

    def add_pending_acknowledgement(self, job_id, device_id):
        self.pending_job_acks[job_id] = device_id
    
    def remove_pending_acknowledgement(self, job_id):
        if job_id in self.pending_job_acks:
            del self.pending_job_acks[job_id]
    
    def cancel_and_reschedule_job(self, job_id):
        
        # TODO: implement cancelling the job for phones. waiting to see what subhash adds for "cancel process" For now, I just call the job a failure and move on. I do not tell the device to cancel.
        job = db.get_job(job_id)
        job_json = job.to_json()

        job = db.update_job(job_json['id'], job.FAILED)
        job.assigned_device_id = None 
        job.save()

        print("Job #", job.id, "cancelled and rescheduled.")

        # Reschedule the job for another device, if and only if the number of retries don't go past 3.
        if job_json["num_rescheduled"] < 3:
            rescheduled_job_spec = {
                "resource_requirements": job_json["resource_requirements"],
                "code_url": job_json["code_url"],
                "num_rescheduled": job_json["num_rescheduled"] + 1
            }
            # rescheduled_job = create_job(rescheduled_job_spec)
            resp = requests.post(submit_job_url, json=rescheduled_job_spec).json()
            print("Response from rescheduling timed out job: ", resp)