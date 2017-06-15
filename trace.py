# -*- coding: utf-8 -*-

import wx
import serial
import time
import logging
from wx.lib.pubsub import pub
from wx.lib.pubsub import setupkwargs

# Import matplotlib for wxPython
#from matplotlib.figure import Figure
#from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas

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
        self.Bind(wx.EVT_PAINT, self.OnPaint)

	traceSizer = self.setup_trace_sizer()
	statusSizer = self.setup_status_sizer()
	nullSizer2 = wx.BoxSizer(wx.VERTICAL)

        topSizer = wx.BoxSizer(wx.VERTICAL)
	topSizer.Add(traceSizer, 0, wx.TOP|wx.LEFT|wx.RIGHT, BORDER1)
	topSizer.Add(statusSizer, 0, wx.TOP|wx.LEFT|wx.RIGHT, BORDER1)
	#topSizer.Add(plotSizer, 0, wx.TOP|wx.LEFT|wx.RIGHT, BORDER1)
	#topSizer.Add(linech, 0, wx.TOP|wx.LEFT|wx.RIGHT, BORDER1)
        self.SetSizer(topSizer)

	pub.subscribe(self.serialListener, 'serialListener')

        logging.basicConfig(format="%(filename)s: %(funcName)s() - %(message)s", level=logging.INFO)

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        dc.DrawRectangle(10, 300, 400, 380)

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

        txtNull = wx.StaticText(self, wx.ID_ANY, ' ')

        self.btnStatus = wx.Button(self, wx.ID_ANY, 'Status')
        self.Bind(wx.EVT_BUTTON, self.onStatus, self.btnStatus)

        statBoxSizer.Add(self.btnStatus, 0, wx.ALL, 20)
        statBoxSizer.Add(statusSizer, 0, wx.ALL, 20)
        statBoxSizer.Add(valueSizer, 0, wx.ALL, 20)
        statBoxSizer.Add(unitSizer, 0, wx.ALL, 20)
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

	# setup trace conditions
        serial_cmd('trace prescaler 10', self.mySer)
	time.sleep(1)
        serial_cmd('trace trig iq > 5.0000 10', self.mySer)
	time.sleep(1)
        serial_cmd('trace selall iq', self.mySer)
	time.sleep(1)

        serial_cmd('e', self.mySer)
	time.sleep(1)
        serial_cmd('brake 0', self.mySer)
	time.sleep(1)
        serial_cmd('speed 10', self.mySer)

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
	rv = serial_read('status', 79, self.mySer)
	print rv
	print '---'
        self.vBatValue.SetLabel(rv[12:18])
        self.motorTempValue.SetLabel(rv[35:40])
        self.driveAValue.SetLabel(rv[53:58])
        self.driveBValue.SetLabel(rv[71:76])

    def DrawAxis(self, dc):
        #dc.SetPen(wx.Pen('#0AB1FF'))
        self.dc.SetPen(wx.Pen('#000000'))
        font = dc.GetFont()
        font.SetPointSize(8)
        self.dc.SetFont(font)
        self.dc.DrawLine(1, 1, 300, 1)
        self.dc.DrawLine(1, 1, 1, 201)

        for i in range(20, 220, 20):
            self.dc.DrawText(str(i), -30, i+5)
            self.dc.DrawLine(2, i, -5, i)

        for i in range(100, 300, 100):
            self.dc.DrawLine(i, 2, i, -5)

