import os
import time
import sys
import subprocess

os.system('./matplot.py&')
time.sleep(2)

# get pid
out = os.popen('pgrep -f matplot.py').readlines()
out2 = out[0].rstrip('\n')

var = raw_input("Enter -> ")

# kill matplotlib
proc = subprocess.Popen(['kill -9 '+out2], stdout=subprocess.PIPE, shell=True)
