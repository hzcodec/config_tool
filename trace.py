# -*- coding: utf-8 -*-

import wx
import serial
import time
import logging
import threading
from wx.lib.pubsub import pub
from wx.lib.pubsub import setupkwargs

RED   = (255, 19, 32)

BORDER1 = 10
BORDER2 = 5

GREY  = (180, 180, 180)
BLACK = (0, 0, 0)

IQ_START = 12
SPEED_START = 13
SET_SPEED_START = 14
END_DATA = 200

# speed threshold value
THRESHOLD_VALUE = 8.0

def serial_cmd(cmd, serial):
    # send command to serial port
    try:
        serial.write(cmd + '\r');
        serial.reset_output_buffer()
    except:
        logging.info('Not connected')


def serial_read(cmd, no, serial):
    # send command to serial port
    serial.reset_input_buffer()
    serial.reset_output_buffer()
    serial.write(cmd+'\r');

    # read data from serial port
    c = serial.read(no)
    return c


class GetTraceData(threading.Thread):

    def __init__(self, serial):
        th = threading.Thread.__init__(self)
	self.ser = serial
	self.fd = open("trace_data.txt", "w")
	self.setDaemon(True)
        self.start()    # start the thread
 
    def run(self):
        serial_cmd('trace prescaler 10', self.ser)
        time.sleep(0.5)
        serial_cmd('trace trig set_speed > 5.0000 10', self.ser)
        time.sleep(0.5)
        serial_cmd('trace selall iq speed set_speed', self.ser)
        time.sleep(0.5)
        serial_cmd('trace reset', self.ser)
        time.sleep(0.5)
         
        # enable drive stage, release brake and start motor at speed 20
        serial_cmd('e', self.ser)
        time.sleep(1)
        serial_cmd('brake 0', self.ser)
        time.sleep(1)
        serial_cmd('speed 20', self.ser)
        time.sleep(2)
        
        # stop motor, set brake and disable drive stage
        serial_cmd('speed 0', self.ser)
        time.sleep(1)
        serial_cmd('brake 1', self.ser)
        time.sleep(1)
        serial_cmd('d', self.ser)
        
        time.sleep(1)
        rv = serial_read('trace dump', 9000, self.ser)
	print rv
	time.sleep(1)
	self.analyze_data(rv)

    def analyze_data(self, trace_data):
        logging.info('')
	splitTraceData = trace_data.split(' ')

        print 20*'-'
	idx = 0
	result = 'OK'

	# extract iq data
	for i in range(IQ_START, END_DATA, 4):
	    # get rid of \r\n
	    extractedIq = splitTraceData[i].replace("\r\n","")
	    print ('[%d] - %s') % (idx, extractedIq)
	    self.fd.write(extractedIq+'\n')
	    idx += 1

        print 20*'-'
	idx = 0

	# extracted speed data
	listSpeed = []
	for i in range(SPEED_START, END_DATA, 4):
	    # get rid of \r\n
	    extractedSpeed = splitTraceData[i].replace("\r\n","")
	    print ('[%d] - %s') % (idx, extractedSpeed)
	    self.fd.write(extractedSpeed + '\n')
	    listSpeed.append(extractedSpeed)
	    idx += 1

	# get threshold value, cast it to float and check
	ff = listSpeed[30]
	gg = float(ff)
	if (gg < THRESHOLD_VALUE):
	    result = 'NOK'

        print 20*'-'
	idx = 0
	# extracted set_speed data
	for i in range(SET_SPEED_START, END_DATA, 4):
	    # get rid of \r\n
	    extractedSetSpeed = splitTraceData[i].replace("\r\n","")
	    print ('[%d] - %s') % (idx, extractedSetSpeed)
	    self.fd.write(extractedSetSpeed+'\n')
	    idx += 1

	self.fd.close()
        wx.CallAfter(pub.sendMessage, "dataListener", msg=result)


class TraceTestForm(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
	
        self.mySer = None
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
        statBoxSizer = wx.StaticBoxSizer(statBoxSerial, wx.HORIZONTAL)

        txtNull = wx.StaticText(self, wx.ID_ANY, ' ')
        self.txtTraceResult = wx.StaticText(self, wx.ID_ANY, 'Trace result:')
        self.txtResult = wx.StaticText(self, wx.ID_ANY, '-')

        self.btnTrace = wx.Button(self, wx.ID_ANY, 'Trace')
        self.Bind(wx.EVT_BUTTON, self.onTrace, self.btnTrace)

        statBoxSizer.Add(self.btnTrace, 0, wx.ALL, 20)
        statBoxSizer.Add(self.txtTraceResult, 0, wx.ALL, 20)
        statBoxSizer.Add(self.txtResult, 0, wx.ALL, 20)
        statBoxSizer.Add(txtNull, 0, wx.LEFT, 750) # this is just to get the statBoxSerial larger 

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

    def setup_plot_sizer(self):
	statBoxSerial = wx.StaticBox(self, wx.ID_ANY, '  Plot result')
	statBoxSerial.SetBackgroundColour(GREY)
	statBoxSerial.SetForegroundColour(BLACK)
        statBoxSizer = wx.StaticBoxSizer(statBoxSerial, wx.HORIZONTAL)

	self.figure = Figure(figsize=(5.0, 4.0), dpi=100)
	self.canvas = FigCanvas(self, -1, self.figure)
	self.ax = self.figure.add_subplot(111)

        statBoxSizer.Add(self.canvas, 0, wx.ALL, 20)

	self.Layout()

	return statBoxSizer

    def serialListener(self, message, fname=None):
        print 'msg:', message
	self.mySer = message

    def onTrace(self, event):

	# start thread
	GetTraceData(self.mySer)

    def onStatus(self, event):
        logging.info('')

	try:
	    rv = serial_read('status', 79, self.mySer)
	    time.sleep(0.2)
	    rv = serial_read('status', 79, self.mySer)
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

    def paint(self):
        dc = wx.PaintDC(self)
	self.x1 = 10
	self.y1 = 300
	self.width = 400
	self.hight = 380
        dc.DrawRectangle(self.x1, self.y1, self.width, self.hight)
	self.draw_axis(dc)

    def draw_axis(self, dc):
        dc.SetPen(wx.Pen('#FF0000'))
	mid = self.y1 + (self.hight / 2)
        dc.DrawLine(self.x1+20, mid, self.width-10, mid)

        #for i in range(20, 220, 20):
        #    dc.DrawText(str(i), -30, i+5)
        #    dc.DrawLine(2, i, -5, i)

        #for i in range(100, 300, 100):
        #    dc.DrawLine(i, 2, i, -5)

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

    def dataListener(self, msg):
        if (msg == 'OK'):
            self.txtResult.SetLabel("Performance OK")
	else:
            self.txtResult.SetLabel("Performance Not OK")

