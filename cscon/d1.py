import multiprocessing
import time

class Worker(multiprocessing.Process):
    def __init__(self, num):
        self.num = num
        multiprocessing.Process.__init__(self)
    def run(self):
        print "hebehube", self.num

for i in range(10):
    a = Worker(i)
    a.start()
    a.join()

