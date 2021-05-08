import psutil
def battery_level():
    """battery level in %"""
    battery = psutil.sensors_battery()
    percent = round(battery.percent,2)
    return percent
def plugged_in():
    """whether or not device is plugged in to power"""
    battery = psutil.sensors_battery()
    return battery.power_plugged
def cpu_use():
    """system-wide cpu use"""
    return psutil.cpu_percent(interval=1)
def disk_use():
    """total disk use in %"""
    return psutil.disk_usage('/').percent
def temp():
    #todo - fill in (device-specific)
    psutil.sensors_temperatures()
