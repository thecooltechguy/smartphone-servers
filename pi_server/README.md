# Quickstart

## Run the backend API server
```shell script
python app.py
```

## Test commands
### Register a new device
This request would be made from the smartphones
```shell script
curl --location --request POST 'http://127.0.0.1:5000/devices/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "id" : "dev1",
    "smart_plug_key" : "<insert IFTTT key here>"
}'
```

Example response:
```json
{
    "success": true
}
```

### List all devices
Note that the registered device will first be inactive until it receives the first heartbeat (with all the metadata info, etc.)
```shell script
curl --location --request GET 'http://127.0.0.1:5000/devices/'
```

Example response:
```json
{
    "devices": [
        {
            "id": "dev1",
            "is_active": false,
            "last_heartbeat": "2021-04-24 11:29:39.252261",
            "metadata": {}
        }
    ],
    "success": true
}
```

### Send a heartbeat
This would be sent from the phones to the server

```shell script
curl --location --request POST 'http://127.0.0.1:5000/devices/dev1/heartbeat/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "system" : {
        "cpu" : 0.8,
        "memory" : 16
    }
}'
```

Example response:
```json
{
    "success": true
}
```

### List all devices
The registered device will now be shown as active (and will remain active for the next 1 minute, while no further heartbeat is sent)
```shell script
curl --location --request GET 'http://127.0.0.1:5000/devices/'
```

Example response:
```json
{
    "devices": [
        {
            "id": "dev1",
            "is_active": true,
            "last_heartbeat": "2021-04-24 11:29:39.252261",
            "metadata": {
                "system": {
                    "cpu": 0.8,
                    "memory": 16
                }
            }
        }
    ],
    "success": true
}
```

### Wait for 1 minute
After this time period, the device becomes inactive again in our backend server

### List all devices
Ensure that the device is now inactive (the `is_active` field should be set to `false` now)
```shell script
curl --location --request GET 'http://127.0.0.1:5000/devices/'
```

Example response:
```json
{
    "devices": [
        {
            "id": "dev1",
            "is_active": false,
            "last_heartbeat": "2021-04-24 11:29:39.252261",
            "metadata": {
                "system": {
                    "cpu": 0.8,
                    "memory": 16
                }
            }
        }
    ],
    "success": true
}
```

### Send another heartbeat
```shell script
curl --location --request POST 'http://127.0.0.1:5000/devices/dev1/heartbeat/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "system" : {
        "cpu" : 0.8,
        "memory" : 16
    }
}'
```

Example response:
```json
{
    "success": true
}
```

### List all devices
Now, the device's status should be active again.

```shell script
curl --location --request GET 'http://127.0.0.1:5000/devices/'
```

Example response:
```json
{
    "devices": [
        {
            "id": "dev1",
            "is_active": true,
            "last_heartbeat": "2021-04-24 11:29:39.252261",
            "metadata": {
                "system": {
                    "cpu": 0.8,
                    "memory": 16
                }
            }
        }
    ],
    "success": true
}
```

## Setting up Wyze Smart Plug
1. Create a Wyze account and connect the smart plug to your account
2. Create a IFTTT account and connect your Wyze account to it
3. Create two IFTTT applets
    - Applet 1: If webhook with "battery_low" event, then turn on the smart plug.
    - Applet 2: If webhook with "battery_high" event, then turn off the smart plug.
4. Find your URL key: https://ifttt.com/maker_webhooks/ and click on Documentation.
5. Use your URL key to register the device through the pi_server

# TODO
- Need to store devices & state in a DB, not in memory