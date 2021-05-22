from peewee import *
from playhouse.sqlite_ext import *
import datetime

db = SqliteDatabase('database.db')

class BaseModel(Model):
    class Meta:
        database = db

class Device(BaseModel):
    metadata = JSONField()

    smart_plug_key = TextField()

    time_created = DateTimeField(default=datetime.datetime.utcnow)
    last_heartbeat = DateTimeField(default=datetime.datetime.utcnow)
    time_updated = DateTimeField()

    num_failed_jobs = IntegerField(default=0)
    num_failed_acks = IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.time_updated = datetime.datetime.utcnow()
        return super(Device, self).save(*args, **kwargs)

    def to_json(self):
        return {
            "id" : self.id,
            "last_heartbeat" : str(self.last_heartbeat),
            "time_created" : str(self.time_created),
            "time_updated" : str(self.time_updated),
            "assigned_jobs" : {
                "num_total" : len(self.assigned_jobs)
            },
            "smart_plug_key" : self.smart_plug_key,
            "metadata" : self.metadata,
            "num_failed_jobs": self.num_failed_jobs,
            "num_failed_acks": self.num_failed_acks
        }


class Job(BaseModel):
    UNASSIGNED = 0
    ASSIGNED = 1
    FAILED = 2
    SUCCEEDED = 3

    status = IntegerField(choices=[(UNASSIGNED, "UNASSIGNED"), (ASSIGNED, "ASSIGNED"), (FAILED, "FAILED"), (SUCCEEDED, "SUCCESS")], default=0)
    assigned_device = ForeignKeyField(Device, backref="assigned_jobs", null=True, default=None)

    # Resource limits
    # -1 means no limit
    cpus = IntegerField(default=-1)
    memory_mb = IntegerField(default=-1)
    max_runtime_secs = IntegerField(default=-1)

    # Specification
    code_url = TextField()

    time_created = DateTimeField(default=datetime.datetime.utcnow)
    time_updated = DateTimeField()

    num_rescheduled = IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.time_updated = datetime.datetime.utcnow()
        return super(Job, self).save(*args, **kwargs)

    def to_json(self):
        return {
            "id" : self.id,
            "status" : self.status,
            "assigned_device_id" : None if not self.assigned_device else self.assigned_device.id,
            "resource_requirements" : {
                "cpus" : self.cpus,
                "memory_mb" : self.memory_mb,
                "max_runtime_secs" : self.max_runtime_secs
            },
            "code_url" : self.code_url,
            "time_created" : str(self.time_created),
            "time_updated" : str(self.time_updated),
            "num_rescheduled" : self.num_rescheduled
        }


def create_device(smart_plug_key, metadata):
    device = Device(smart_plug_key=smart_plug_key, metadata=metadata)
    device.save()
    return device.id

def create_job(job_spec):
    assert "resource_requirements" in job_spec and "code_url" in job_spec
    job = Job(status=Job.UNASSIGNED,
              cpus=job_spec["resource_requirements"].get("cpus", -1),
              memory_mb=job_spec["resource_requirements"].get("memory_mb", -1),
              max_runtime_secs=job_spec["resource_requirements"].get("max_runtime_secs", -1),
              code_url = job_spec['code_url'],
              num_rescheduled = job_spec.get("num_rescheduled", 0))
    job.save()
    return job

def get_device(device_id):
    try:
        return Device.get(Device.id == device_id)
    except:
        return None

def get_devices_not_currently_in_use():
    # TODO: A more optimized query would involve JOINS, but for now, we're doing it the naive way
    return [device for device in get_all_devices() if len(device.assigned_jobs) == 0]

def get_all_devices():
    return list(Device.select())

def get_all_jobs():
    return list(Job.select())

def get_job(job_id):
    try:
        return Job.get(Job.id == job_id)
    except:
        return None

def update_device(device_id, metadata):
    device = get_device(device_id=device_id)
    device.metadata = metadata
    device.save()

def update_job(job_id, status):
    job = get_job(job_id=job_id)
    job.status = status
    return job

def assign_jobs():
    # TODO:
    pass

