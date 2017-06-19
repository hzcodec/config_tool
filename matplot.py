#!/usr/bin/env python
import sys
import matplotlib.pyplot as plt

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


SAMPLE_TIME = 83.0    # sample time in us
MAX_LEVEL = 30.0      # max level when trigger is reached
EXPAND_WINDOW = 1.1   # expand matplot window
X_POS = 0.2           # x-position of alpha print out
Y_POS = 0.6           # y-position of alpha print out
SPACE = 11

t = []

# read in data file
def read_indata():

    with open('speed_data1.txt') as f:
        content = f.readlines()

    content = [x.strip() for x in content]

    # convert to float
    result = map(float, content)

    # number of lines
    n = sum(1 for line in open('speed_data1.txt'))

    #print bcolors.GREEN + '  Max input value: ', str(max(result)) + bcolors.ENDC

    return content, n

def read_indata2():

    with open('speed_data2.txt') as f:
        content = f.readlines()

    content = [x.strip() for x in content]

    # convert to float
    result = map(float, content)

    # number of lines
    n = sum(1 for line in open('speed_data2.txt'))

    return content, n


###################################################################
def main():

    data1, numberOfLines1 = read_indata()
    data2, numberOfLines2 = read_indata2()
    
    t = range(numberOfLines1)
    #res = [x*SAMPLE_TIME/1000.0 for x in t]
   
    ## make space for the curve
    #plt.ylim(float(min(data2))*EXPAND_WINDOW, float(max(data1))*EXPAND_WINDOW)
    
    # set window title
    plt.gcf().canvas.set_window_title('Performance test')
    
    plt.plot(t, data1, color="blue", linewidth=1, marker='.', linestyle='-')
    plt.plot(t, data2, color="red", linewidth=1, marker='.', linestyle='-')
    
    #legends
    plt.legend(loc='upper left', frameon=False)
    
    plt.xlabel('[s]')
    
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()
