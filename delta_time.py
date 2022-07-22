import time

class DeltaTime():
    def __init__(self):
        self.start_time=time.time()
        self.end_time=time.time()
    
    def reset(self):
        self.start_time=time.time()
    
    def stop(self):
        self.end_time=time.time()
    
    def getDeltaTime(self):
        self.stop()
        return self.end_time-self.start_time
    
    def getDifferentTime(self):
        return self.end_time-self.start_time