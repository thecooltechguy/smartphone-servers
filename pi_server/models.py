from datetime import datetime, timedelta
import power

# number of minutes in between heart beats that still considers the device is alive and healthy
HEARTBEAT_ACTIVE_RANGE_MINUTES = 1

class Phone:
    def __init__(self, id, key):
        self.id = id
        self.last_heartbeat = None
        self.metadata = None
        self.smart_plug_key = key

    @property
    def is_active(self):
        if not self.last_heartbeat:
            return False
        return datetime.utcnow() - self.last_heartbeat <= timedelta(minutes=HEARTBEAT_ACTIVE_RANGE_MINUTES)

    def to_json(self):
        return {
            "id" : self.id,
            "last_heartbeat" : str(self.last_heartbeat),
            "is_active" : self.is_active,
            "metadata" : self.metadata
        }

    def stop_charging(self):
        power.power_off(self.smart_plug_key)
        
    def start_charging(self):
        power.power_on(self.smart_plug_key)
