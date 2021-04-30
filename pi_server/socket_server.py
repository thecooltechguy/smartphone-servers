import websockets
import threading
import asyncio
import socket
import time

# represents the Task class for now
class Task:
    def __init__(self, github_link):
        self.github_link = github_link

class SocketServer(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)

        # keeps track of the tasks per device and their socket #
        self.device_tasks = {}
        self.device_sockets = {}

        # the server's listening port
        self.port = port

        # to stop sending tasks
        self.stop = False
        print(port)

        threading.Thread(target = self.handleSendingTasks).start()
        
    def run(self):
        
        # setup the socket to localhost and defined port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", self.port))
        s.listen()

        # keep accepting connections for new devices.
        while not stop:
            conn, addr = s.accept()
            print("Connected by:", addr)

            # phone should return device id
            device_id = conn.recv(1024)
            device_id = device_id.decode("utf-8")
            print("Device ID from Phone: ", device_id)

            # only add a list if they're not in the tasks (phones that disconnected 
            # their sockets should be able to reconnect and have the same tasks)
            if device_id not in self.device_tasks:
                self.device_tasks[device_id] = []

            # update the socket variable for this device id.
            self.device_sockets[device_id] = conn

    # A separate thread will handle sending tasks to the different phones connected via socket
    def handleSendingTasks(self):
        while True:
            if not stop:

                # for each device, send a single task from their list
                for device in self.device_tasks:
                    if len(self.device_tasks[device]) > 0:
                        task = self.device_tasks[device].pop()
                        self.device_sockets[device].sendall(bytes(task.github_link, 'utf-8'))

                # wait 10 seconds until we check again for new tasks... 
                # will replace with more complex algo later
                time.sleep(10)
            else:
                return

    # the raspberry pi will call this with the device id to send a task to the phone
    def sendTask(self, device_id, task):
        if device_id not in self.device_tasks:
            print("No device ID for addTask")
            return
        self.device_tasks[device_id].append(task)
    
    # used to stop the pi from sending data
    def stop(self):
        self.stop = True
