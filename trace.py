import wx
import serial
import time
import logging
from wx.lib.pubsub import pub
from wx.lib.pubsub import setupkwargs

BORDER1 = 10

GREY  = (180, 180, 180)
BLACK = (0, 0, 0)

def serial_cmd(cmd, serial):
    # send command to serial port
    try:
        serial.write(cmd + '\r');
    except:
        logging.info('Not connected')

class TraceTestForm(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.mySer = None

	alignSizer = self.setup_trace_sizer()
	nullSizer2 = wx.BoxSizer(wx.VERTICAL)

        topSizer = wx.BoxSizer(wx.VERTICAL)
	topSizer.Add(alignSizer, 0, wx.TOP|wx.LEFT|wx.RIGHT, BORDER1)
	#topSizer.Add(nullSizer2, 0, wx.TOP|wx.LEFT, BORDER1)
        self.SetSizer(topSizer)

	pub.subscribe(self.serialListener, 'serialListener')

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

        self.btnStatus = wx.Button(self, wx.ID_ANY, 'Status')
        self.Bind(wx.EVT_BUTTON, self.onStatus, self.btnStatus)

        statBoxSizer.Add(self.btnTrace, 0, wx.ALL, 20)
        statBoxSizer.Add(self.btnStop, 0, wx.ALL, 20)
        statBoxSizer.Add(self.btnDump, 0, wx.ALL, 20)
        statBoxSizer.Add(self.btnStatus, 0, wx.ALL, 20)
        statBoxSizer.Add(txtNull, 0, wx.LEFT, 650) # this is just to get the statBoxSerial larger 

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
        serial_cmd('status', self.mySer)

