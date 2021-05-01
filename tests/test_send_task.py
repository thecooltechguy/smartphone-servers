import requests

add_task_url = "http://192.168.0.113:5000/devices/addTask/"

data = {"github_link": "https://github.com/jfswitzer/ut_test.git"}

y = requests.post(add_task_url, data=data)
print(y.text)
