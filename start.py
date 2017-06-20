import os
import time
import sys
import subprocess
import threading

class PollAlignment(threading.Thread):

    def __init__(self):
        th = threading.Thread.__init__(self)
	self.setDaemon(True)
        self.start()    # start the thread
 
    def run(self):
        os.system('./matplot.py&')


def main():

    PollAlignment()
    time.sleep(0.5)

    # get pid
    out = os.popen('pgrep -f matplot.py').readlines()
    out2 = out[0].rstrip('\n')

    
    var = raw_input("Enter -> ")
    
    # kill matplotlib
    proc = subprocess.Popen(['kill -9 '+out2], stdout=subprocess.PIPE, shell=True)


if __name__ == '__main__':
    main()
