import os
import subprocess
        
class TaskManager():
    def __init__(self):
        self.tasks = []
    def task_init(self,repo,max_cpu=1, max_ram=1,max_disc=4, max_runtime=60):
        """repo is link to github repo that contains the task; kicks off task; returns pid"""
        self.tasks.append(Task(repo,max_cpu, max_ram,max_disc, max_runtime))
        
class Task():
    def __init__(self,repo,max_cpu, max_ram,max_disc, max_runtime):
        self.max_cpu = max_cpu
        self.max_ram = max_ram
        self.max_disc = max_disc
        self.max_runtime = max_runtime
        self.name = repo[:-4].split('/')[-1]
        process = subprocess.Popen(['git', 'clone', repo],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if 'fatal' in str(stderr): #does this catch all errors?
            print(stderr)
            raise Exception("Failed to clone repo: "+repo)
        process = subprocess.call(self.name+"/main.sh",shell=True)
        self.state = "running"
    def check_task(self):
        pass

tm = TaskManager()
tm.task_init('https://github.com/jfswitzer/ut_test.git')
                
