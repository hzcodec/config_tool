# -*- coding: utf-8 -*-

import wx
import serial
import time
import logging
from wx.lib.pubsub import pub
from wx.lib.pubsub import setupkwargs

RED   = (255, 19, 32)

BORDER1 = 10
BORDER2 = 5

GREY  = (180, 180, 180)
BLACK = (0, 0, 0)

def serial_cmd(cmd, serial):
    # send command to serial port
    try:
        serial.write(cmd + '\r');
    except:
        logging.info('Not connected')


def serial_read(cmd, no, serial):
    # send command to serial port
    serial.write(cmd+'\r');
    serial.reset_input_buffer()
    serial.reset_output_buffer()
    serial.flush()

    # read data from serial port
    c = serial.read(no)
    return c


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
	#topSizer.Add(plotSizer, 0, wx.TOP|wx.LEFT|wx.RIGHT, BORDER1)
        self.SetSizer(topSizer)

	pub.subscribe(self.serialListener, 'serialListener')
	pub.subscribe(self.configListener, 'configListener')

        logging.basicConfig(format="%(filename)s: %(funcName)s() - %(message)s", level=logging.INFO)

    def setup_trace_sizer(self):
	statBoxSerial = wx.StaticBox(self, wx.ID_ANY, '  Trace test')
	statBoxSerial.SetBackgroundColour(GREY)
	statBoxSerial.SetForegroundColour(BLACK)
        statBoxSizer = wx.StaticBoxSizer(statBoxSerial, wx.HORIZONTAL)

        txtNull = wx.StaticText(self, wx.ID_ANY, ' ')

        self.btnTrace = wx.Button(self, wx.ID_ANY, 'Trace')
        self.Bind(wx.EVT_BUTTON, self.onTrace, self.btnTrace)

        self.btnStop = wx.Button(self, wx.ID_ANY, 'Stop')
        self.Bind(wx.EVT_BUTTON, self.onStop, self.btnStop)

        self.btnDump = wx.Button(self, wx.ID_ANY, 'Dump')
        self.Bind(wx.EVT_BUTTON, self.onDump, self.btnDump)

        statBoxSizer.Add(self.btnTrace, 0, wx.ALL, 20)
        statBoxSizer.Add(self.btnStop, 0, wx.ALL, 20)
        statBoxSizer.Add(self.btnDump, 0, wx.ALL, 20)
        statBoxSizer.Add(txtNull, 0, wx.LEFT, 650) # this is just to get the statBoxSerial larger 

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
        logging.info('')

	try:
	    # setup trace conditions
            serial_cmd('trace prescaler 10', self.mySer)
	    time.sleep(0.5)
            serial_cmd('trace trig iq > 5.0000 10', self.mySer)
	    time.sleep(0.5)
            serial_cmd('trace selall iq', self.mySer)
	    time.sleep(0.5)
            serial_cmd('trace reset', self.mySer)
	    time.sleep(0.5)

            serial_cmd('e', self.mySer)
	    time.sleep(1)
            serial_cmd('brake 0', self.mySer)
	    time.sleep(1)
            serial_cmd('speed 10', self.mySer)

	except:
	    print 'Data could not be read. Check current connection to serial port.'

    def onStop(self, event):
        logging.info('')
        serial_cmd('speed 0', self.mySer)
	time.sleep(1)
        serial_cmd('brake 1', self.mySer)
	time.sleep(1)
        serial_cmd('d', self.mySer)

    def onDump(self, event):
        logging.info('')
        serial_cmd('trace dump', self.mySer)

    def onStatus(self, event):
        logging.info('')

	try:
	    rv = serial_read('status', 79, self.mySer)
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

	except:
	    print 'Data could not be read. Check current connection to serial port.'

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

