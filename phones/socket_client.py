import socket
import threading

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 2222        # The port used by the server

# represents the Task class for now
class Task:
    def __init__(self, github_link):
        self.github_link = github_link

class SocketClient (threading.Thread):
    def __init__(self, device_id):
        threading.Thread.__init__(self)

        # self.socket used to receive data from and send data to pi
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(bytes(device_id, 'utf-8'))
        self.socket = s

        # pending tasks
        self.tasks = []
        
    def run(self):
        while True:
            data = self.socket.recv(1024)
            print('Received', repr(data))

            if data:
                # for now it's just a task with some github link
                self.tasks.append(Task(data.decode('utf-8')))
    
    def getNextTask(self):
        if len(self.tasks) > 0:
            return self.tasks.pop()
        else:
            return None