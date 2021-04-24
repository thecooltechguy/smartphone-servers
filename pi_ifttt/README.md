# Smart Phone Data Center


# Setting up Wyze Smart Plug
1. Create a Wyze account and connect the smart plug to your account
2. Create a IFTTT account and connect your Wyze account to it
3. Create two IFTTT applets
    - Applet 1: If webhook with "battery_low" event, then turn on the smart plug.
    - Applet 2: If webhook with "battery_high" event, then turn off the smart plug.
4. Find your URL key: https://ifttt.com/maker_webhooks/ and click on Documentation.
5. Use your URL key to run power.py (Usage:  python power.py [on, off] [key])