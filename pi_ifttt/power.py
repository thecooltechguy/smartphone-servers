import requests
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python power.py [on, off] [key]")
        exit(1)
    on_command = sys.argv[1] == "on"
    off_command = sys.argv[1] == "off"
    if not on_command and not off_command:
        print("Usage: python power.py [on, off] [key]")
        exit(1)
    
    if on_command:
        print("Power On Command Sent")
        requests.get("https://maker.ifttt.com/trigger/battery_low/with/key/" + sys.argv[2])

    if off_command:
        print("Power Off Command Sent")
        requests.get("https://maker.ifttt.com/trigger/battery_high/with/key/" + sys.argv[2])
