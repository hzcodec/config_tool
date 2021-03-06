# -*- coding: utf-8 -*-

import wx
import serial
import time
import logging
import threading
from wx.lib.pubsub import pub
from wx.lib.pubsub import setupkwargs
import select
import sys
import os

RED   = (255, 19, 32)

BORDER1 = 10
BORDER2 = 5

GREY  = (180, 180, 180)
BLACK = (0, 0, 0)

TRACE_DATA_START = 4
SPEED_START = 13
SET_SPEED_START = 14
END_DATA = 200


# speed threshold value
THRESHOLD_VALUE = 8.0
TARGET_SPEED1 = 19.9
TARGET_SPEED2 = -19.9

# time delay until speed is reached its target speed
TIME_DELAY = '170'


def serial_cmd(cmd, serial):
    # send command to serial port
    try:
        serial.write(cmd + '\r');
        serial.reset_output_buffer()
    except:
        logging.info('Not connected')


def serial_read(cmd, serial):
    # send command to serial port
    serial.reset_input_buffer()
    serial.reset_output_buffer()
    serial.write(cmd+'\r');

    cnt = 0
    tracedData = []

    while True:
        line = serial.readline()
	cnt += 1
        #print cnt, line,
	tracedData.append(line)

	if (cnt > 240):
	    break

    return tracedData


def serial_read2(cmd, no, serial):
    # send command to serial port
    serial.reset_input_buffer()
    serial.reset_output_buffer()
    serial.write(cmd+'\r');

    # read data from serial port
    c = serial.read(no)
    return c


class MatPlot(threading.Thread):

    def __init__(self):
        th = threading.Thread.__init__(self)

	self.setDaemon(True)
        self.start()    # start the thread
 
    def run(self):
	logging.info('Launching matplot')
	self.dirPath = os.getcwd()
	print 'dirPath in Matplot:', self.dirPath + '/Desktop'
        os.system(self.dirPath + '/Desktop/matplot.py&')


class GetTraceData(threading.Thread):

    def __init__(self, serial):
        th = threading.Thread.__init__(self)
	self.ser = serial

	# find current path for application
	dirPath = os.getcwd()
        filePath = dirPath + '/Desktop/logdata'
	print 'filePath for logdata:', filePath

	# create log directory
	try:
	    os.stat(filePath)
	    print 'Logfile dir exists'
	except:
	    print 'Logfile dir created'
	    os.mkdir(filePath)

	logging.info('Open iq1 data file')
	self.fdIqData1 = open(filePath + '/iq_data1.txt', 'w')

	logging.info('Open speedData1 data file')
	self.fdSpeedData1 = open(filePath + '/speed_data1.txt', 'w')

	logging.info('Open SetspeedData1 data file')
	self.fdSetSpeedData1 = open(filePath + '/set_speed_data1.txt', 'w')

	logging.info('Open iq2 data file')
	self.fdIqData2 = open(filePath + '/iq_data2.txt', 'w')

	logging.info('Open speedData2 data file')
	self.fdSpeedData2    = open(filePath + '/speed_data2.txt', 'w')

	logging.info('Open setSpeedData2 data file')
	self.fdSetSpeedData2 = open(filePath + '/set_speed_data2.txt', 'w')

	self.setDaemon(True)
        self.start()    # start the thread
 
    def run(self):
        """
	    Run motor up for 2 seconds at speed 20. Then run notor down for 2 seconds at speed -20.
	    Get trace dump after each run.
        """
        serial_cmd('trace prescaler 10', self.ser)
        time.sleep(0.5)
        serial_cmd('trace trig set_speed > 5.0000 10', self.ser)
        time.sleep(0.5)
        serial_cmd('trace selall iq speed set_speed', self.ser)
        time.sleep(0.5)
        serial_cmd('trace reset', self.ser)
        time.sleep(0.5)
         
        # enable drive stage, release brake and start motor at speed 20
	self.enable_motor()
        serial_cmd('speed 20', self.ser)
        time.sleep(2)
        
	self.stop_motor()
        
	# get trace dump values
        time.sleep(1)
        logging.info('Get trace dump 1')
        rv = serial_read('trace dump', self.ser)
	time.sleep(1)

	# reset dump area and set new trigger
        serial_cmd('trace reset', self.ser)
        time.sleep(0.5)
        serial_cmd('trace trig set_speed < -5.0000 10', self.ser)
        time.sleep(0.5)

        # enable drive stage, release brake and start motor at speed -20
	self.enable_motor()
        serial_cmd('speed -20', self.ser)
        time.sleep(2)

        self.stop_motor()

	# get trace dump values
        logging.info('Get trace dump 2')
        rv2 = serial_read('trace dump', self.ser)
	time.sleep(1)

	self.analyze_data(rv, rv2)

    def enable_motor(self):
        serial_cmd('e', self.ser)
        time.sleep(1)
        serial_cmd('brake 0', self.ser)
        time.sleep(1)

    def stop_motor(self):
        serial_cmd('speed 0', self.ser)
        time.sleep(1)
        serial_cmd('brake 1', self.ser)
        time.sleep(1)
        serial_cmd('d', self.ser)

    def analyze_data(self, traceData1, traceData2):
        logging.info('')

	idx = 0
	result = 'NOK'                # flag indicating if threshold is met or not
	targetForSpeed1Reached = 0    # target reached indicator, at least 20 before we consider a valid state
	targetForSpeed2Reached = 0

	listTraceData1 = []

	# split trace data
	for i in range(TRACE_DATA_START, len(traceData1)):
	    splitTraceData = traceData1[i].split(' ')
	    listTraceData1.append(splitTraceData)
	    #print ('[%d] - %s') % (i, listTraceData1[idx])
	    idx += 1

	for i in range(0, len(listTraceData1)):
	    #print ('iq1 - [%d] -> %s') % (i, listTraceData1[i][0])
	    self.fdIqData1.write(listTraceData1[i][0]+'\n')
        self.fdIqData1.close()	

	for i in range(0, len(listTraceData1)):
	    self.fdSpeedData1.write(listTraceData1[i][1]+'\n')

	    if (float(listTraceData1[i][1]) > TARGET_SPEED1):
		targetForSpeed1Reached += 1
	    #print ('[%d] -> %s') % (i, listTraceData1[i][1])

        # close file for speed
        self.fdSpeedData1.close()	

	for i in range(0, len(listTraceData1)):
	    self.fdSetSpeedData1.write(listTraceData1[i][2]+'\n')
	    #print ('[%d] -> %s') % (i, listTraceData1[i][2])
        self.fdSetSpeedData1.close()	

	listTraceData2 = []
	idx = 0

	# split trace data
	for i in range(TRACE_DATA_START, len(traceData2)):
	    splitTraceData = traceData2[i].split(' ')
	    listTraceData2.append(splitTraceData)
	    #print ('[%d] - %s') % (i, listTraceData2[idx])
	    idx += 1

	for i in range(0, len(listTraceData2)):
	    self.fdIqData2.write(listTraceData2[i][0]+'\n')
	    #print ('iq2 - [%d] - %s') % (i, listTraceData2[i][0])
        self.fdIqData2.close()	

	for i in range(0, len(listTraceData2)):
	    self.fdSpeedData2.write(listTraceData2[i][1]+'\n')

	    if (float(listTraceData2[i][1]) > TARGET_SPEED2):
		targetForSpeed2Reached += 1
	    #print ('[%d] - %s') % (i, listTraceData2[i][1])

        # close file for speed
        self.fdSpeedData2.close()	

	for i in range(0, len(listTraceData2)):
	    self.fdSetSpeedData2.write(listTraceData2[i][2]+'\n')
	    #print ('[%d] - %s') % (i, listTraceData2[i][2])
        self.fdSetSpeedData2.close()	

	# at least a number of hits, this is to filter out a glitch
	if (targetForSpeed1Reached > 20 and targetForSpeed2Reached > 20):
	    result = 'OK'

        wx.CallAfter(pub.sendMessage, "dataListener", msg=listTraceData1, msg2=listTraceData2)


class TraceTestForm(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
	
        self.mySer = None
	self.applicationIsConnected = False
        #self.Bind(wx.EVT_PAINT, self.OnPaint)

	traceSizer = self.setup_trace_sizer()
	statusSizer = self.setup_status_sizer()
	nullSizer2 = wx.BoxSizer(wx.VERTICAL)

        topSizer = wx.BoxSizer(wx.VERTICAL)
	topSizer.Add(traceSizer, 0, wx.TOP|wx.LEFT|wx.RIGHT, BORDER1)
	topSizer.Add(statusSizer, 0, wx.TOP|wx.LEFT|wx.RIGHT, BORDER1)
        self.SetSizer(topSizer)

	pub.subscribe(self.serialListener, 'serialListener')
	pub.subscribe(self.configListener, 'configListener')
	pub.subscribe(self.dataListener, 'dataListener')

        logging.basicConfig(format="%(filename)s: %(funcName)s() - %(message)s", level=logging.INFO)

    def setup_trace_sizer(self):
	statBoxSerial = wx.StaticBox(self, wx.ID_ANY, '  Trace test')
	statBoxSerial.SetBackgroundColour(GREY)
	statBoxSerial.SetForegroundColour(BLACK)
        statBoxSizer = wx.StaticBoxSizer(statBoxSerial, wx.VERTICAL)

        txtNull = wx.StaticText(self, wx.ID_ANY, ' ')

        self.btnTrace = wx.Button(self, wx.ID_ANY, 'Trace')
        self.Bind(wx.EVT_BUTTON, self.onTrace, self.btnTrace)

        staticTxtTraceResult = wx.StaticText(self, wx.ID_ANY, 'Trace result:')
        self.staticTxtResult = wx.StaticText(self, wx.ID_ANY, '---')

        timeDelay = wx.StaticText(self, wx.ID_ANY, '               Delay [ms]')
        self.txtCtrl_time_delay = wx.TextCtrl(self, wx.ID_ANY, TIME_DELAY)
        boxTimeDelSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.staticTxtFinalResult1 = wx.StaticText(self, wx.ID_ANY, 'Reached delay (+) :')
        self.staticTxtFinalResult2 = wx.StaticText(self, wx.ID_ANY, 'Reached delay (-) :')
        self.staticTxtReachedPos = wx.StaticText(self, wx.ID_ANY, '---')
        self.staticTxtReachedNeg = wx.StaticText(self, wx.ID_ANY, '---')

	box1 = wx.BoxSizer(wx.HORIZONTAL)
	box2 = wx.BoxSizer(wx.HORIZONTAL)
	box3 = wx.BoxSizer(wx.HORIZONTAL)
	box4 = wx.BoxSizer(wx.HORIZONTAL)

	box1.Add(self.btnTrace, 0, wx.TOP, 20)
	box1.Add(timeDelay, 0, wx.TOP|wx.LEFT, 25)
	box1.Add(self.txtCtrl_time_delay, 0, wx.TOP|wx.LEFT, 21)
	box2.Add(staticTxtTraceResult, 0, wx.TOP|wx.LEFT, 15)
	box2.Add(self.staticTxtResult, 0, wx.TOP|wx.LEFT, 15)
	box3.Add(self.staticTxtFinalResult1, 0, wx.TOP|wx.LEFT, 15)
	box3.Add(self.staticTxtReachedPos, 0, wx.TOP|wx.LEFT, 15)
	box4.Add(self.staticTxtFinalResult2, 0, wx.TOP|wx.LEFT, 15)
	box4.Add(self.staticTxtReachedNeg, 0, wx.TOP|wx.LEFT, 15)

        statBoxSizer.Add(box1, 0, wx.LEFT, 20)
        statBoxSizer.Add(box2, 0, wx.LEFT, 10)
        statBoxSizer.Add(box3, 0, wx.LEFT, 10)
        statBoxSizer.Add(box4, 0, wx.LEFT, 10)
        statBoxSizer.Add(txtNull, 0, wx.LEFT, 1050) # this is just to get the statBoxSerial larger 

	return statBoxSizer

    def configListener(self, message, fname=None):
        logging.info('Loaded parameters %s', message)
	self.configParameters = message

    def setup_status_sizer(self):
	statBoxSerial = wx.StaticBox(self, wx.ID_ANY, '  Status')
	statBoxSerial.SetBackgroundColour(GREY)
	statBoxSerial.SetForegroundColour(BLACK)
        statBoxSizer = wx.StaticBoxSizer(statBoxSerial, wx.HORIZONTAL)

        self.vBatHeadline = wx.StaticText(self, -1, "Vbat:")
        self.motorTempHeadline = wx.StaticText(self, -1, "Motor temp:")
        self.driveAHeadline = wx.StaticText(self, -1, "Drive A temp:")
        self.driveBHeadline = wx.StaticText(self, -1, "Drive B temp:")
	statusSizer = wx.BoxSizer(wx.VERTICAL)
	statusSizer.Add(self.vBatHeadline, 0, wx.ALL, BORDER2)
	statusSizer.Add(self.motorTempHeadline, 0, wx.ALL, BORDER2)
	statusSizer.Add(self.driveAHeadline, 0, wx.ALL, BORDER2)
	statusSizer.Add(self.driveBHeadline, 0, wx.ALL, BORDER2)

        self.vBatValue = wx.StaticText(self, -1, '0')
        self.motorTempValue = wx.StaticText(self, -1, '0')
        self.driveAValue = wx.StaticText(self, -1, '0')
        self.driveBValue = wx.StaticText(self, -1, '0')
	valueSizer = wx.BoxSizer(wx.VERTICAL)
	valueSizer.Add(self.vBatValue, 0, wx.ALL, BORDER2)
	valueSizer.Add(self.motorTempValue, 0, wx.ALL, BORDER2)
	valueSizer.Add(self.driveAValue, 0, wx.ALL, BORDER2)
	valueSizer.Add(self.driveBValue, 0, wx.ALL, BORDER2)

        stringData = '°C'
	unicodeData = unicode(stringData, 'utf-8')

        self.vBatUnit = wx.StaticText(self, -1, 'V')
        self.motorTempUnit = wx.StaticText(self, -1, unicodeData)
        self.driveAUnit = wx.StaticText(self, -1, unicodeData)
        self.driveBUnit = wx.StaticText(self, -1, unicodeData)
	unitSizer = wx.BoxSizer(wx.VERTICAL)
	unitSizer.Add(self.vBatUnit, 0, wx.ALL, BORDER2)
	unitSizer.Add(self.motorTempUnit, 0, wx.ALL, BORDER2)
	unitSizer.Add(self.driveAUnit, 0, wx.ALL, BORDER2)
	unitSizer.Add(self.driveBUnit, 0, wx.ALL, BORDER2)

        self.vBatOk = wx.StaticText(self, -1, ' ')
        self.tempOk = wx.StaticText(self, -1, 'Max motor temp OK')
        self.driveTempAOk = wx.StaticText(self, -1, 'Drive A temp OK')
        self.driveTempBOk = wx.StaticText(self, -1, 'Drive B temp OK')
	tempSizer = wx.BoxSizer(wx.VERTICAL)
	tempSizer.Add(self.vBatOk, 0, wx.ALL, BORDER2)
	tempSizer.Add(self.tempOk, 0, wx.ALL, BORDER2)
	tempSizer.Add(self.driveTempAOk, 0, wx.ALL, BORDER2)
	tempSizer.Add(self.driveTempBOk, 0, wx.ALL, BORDER2)

        txtNull = wx.StaticText(self, wx.ID_ANY, ' ')

        self.btnStatus = wx.Button(self, wx.ID_ANY, 'Status')
        self.Bind(wx.EVT_BUTTON, self.onStatus, self.btnStatus)

        statBoxSizer.Add(self.btnStatus, 0, wx.ALL, 20)
        statBoxSizer.Add(statusSizer, 0, wx.ALL, 20)
        statBoxSizer.Add(valueSizer, 0, wx.ALL, 20)
        statBoxSizer.Add(unitSizer, 0, wx.ALL, 20)
        statBoxSizer.Add(tempSizer, 0, wx.ALL, 20)
        statBoxSizer.Add(txtNull, 0, wx.LEFT, 880) # this is just to get the statBoxSerial larger 

	return statBoxSizer

    def serialListener(self, message, fname=None):
        #print 'msg:', message
	self.applicationIsConnected = True
	self.mySer = message

    def onTrace(self, event):

	if (self.applicationIsConnected == True):

	    # start thread
            self.staticTxtResult.SetLabel("Performance test initiated")
            print "Performance test initiated"
	    GetTraceData(self.mySer)

	else:
            self.staticTxtResult.SetLabel("No connection to serial port")
            print "No connection to serial port"
	    pass

    def onStatus(self, event):
        logging.info('')

	try:
	    rv = serial_read2('status', 79, self.mySer)
	    time.sleep(0.2)
	    rv = serial_read2('status', 79, self.mySer)
	    print 'Status return', rv

            self.vBatValue.SetLabel(rv[12:18])
            self.motorTempValue.SetLabel(rv[35:40])
            self.driveAValue.SetLabel(rv[53:58])
            self.driveBValue.SetLabel(rv[71:76])

	    maxMotorTemp, maxDriveTemp = self.get_values()
	    currentMotorTemp = float(rv[35:40])
	    currentDriveTempA = float(rv[53:58])
	    currentDriveTempB = float(rv[71:76])

	    if (currentMotorTemp > maxMotorTemp):
	        self.tempOk.SetForegroundColour(RED)
	        self.tempOk.SetLabel("Motor temp to high")

	    if (currentDriveTempA > maxDriveTemp):
	        self.driveTempAOk.SetForegroundColour(RED)
	        self.driveTempAOk.SetLabel("Drive A temp to high")

	    if (currentDriveTempB > maxDriveTemp):
	        self.driveTempBOk.SetForegroundColour(RED)
	        self.driveTempBOk.SetLabel("Drive B temp to high")

	except AttributeError:
	    print 'No config file has been read. Comparison not possible'

    def get_values(self):
        """
	    Get current configuration parameters for max motor and max drive temp.
	"""
        logging.info('')

        rv = filter(lambda element: 'max_motor_temp' in element, self.configParameters)
        b = rv[0].split(',')
        maxMotorTemp =  float(b[1])

        rv = filter(lambda element: 'max_drive_temp' in element, self.configParameters)
        b = rv[0].split(',')
        maxDriveTemp =  float(b[1])

	return maxMotorTemp, maxDriveTemp

    def dataListener(self, msg, msg2):

        rv = self.find_idx(msg)
        rv2 = self.find_idx2(msg2)

	timeFactor  = 1/12.0*10.0*rv  # ms * rv
	timeFactor2 = 1/12.0*10.0*rv2 # ms * rv2
	#print 'timeFactor:', timeFactor

	delay = int(self.txtCtrl_time_delay.GetValue())
	#print 'Max delay:', delay
	timeDelay = int(delay*12.0/10.0)

        logging.info('Reached delay for speed1=%.1f ms' % timeFactor)
        logging.info('Reached delay for speed2=%.1f ms' % timeFactor2)

	roundedTimeFactor = round(timeFactor, 1)
	roundedTimeFactor2 = round(timeFactor2, 1)

	# print out result
	unicodeData = unicode(str(roundedTimeFactor), 'utf-8')
        self.staticTxtReachedPos.SetLabel(unicodeData)
	unicodeData = unicode(str(roundedTimeFactor2), 'utf-8')
        self.staticTxtReachedNeg.SetLabel(unicodeData)
        
        if (rv > timeDelay or rv2 > timeDelay):
            self.staticTxtResult.SetLabel("Performance test Not OK")
            print "Performance test Not OK"
	else:
            self.staticTxtResult.SetLabel("Performance test OK")
            print "Performance test OK"

        self.plot_result()

    def plot_result(self):
        MatPlot()
        time.sleep(0.5)

    def find_idx(self, msg):
        """
	    Find first time target speed is reached.
        """
        for idx in range(0, len(msg)):
            #print idx, msg[idx][1]
            if (float(msg[idx][1]) > TARGET_SPEED1):
                return idx
    
        return 0

    def find_idx2(self, msg):
        """
	    Find first time target speed is reached.
        """
        for idx in range(0, len(msg)):
            #print idx, msg[idx][1]

            if (float(msg[idx][1]) < TARGET_SPEED2):
                return idx
    
        return 0
