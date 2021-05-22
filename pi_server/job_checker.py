import threading
from db import *

class JobChecker:

    def __init__(self):
        self.jobs = []
        self.stopped = False

    def check_job(self):
        while not self.stopped:
            currentJobs = db.db.get_all_jobs()

    def stop(self):
        self.stopped = True

    def run(self):
        t1 = threading.Thread(target=self.check_job)
        t1.start()
        t1.join() # runs forever