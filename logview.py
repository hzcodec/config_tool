import wx
import logging
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub


# setup logging function
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s : %(funcName)s() - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def serial_read(cmd, no, serial):
    # send command to serial port
    serial.write(cmd+'\r');

    #serial.reset_input_buffer()
    serial.reset_output_buffer()
    serial.flush()

    # read data from serial port
    c = serial.read(no)
    if (len(c) == 0):
        return 'NO CONN'
    else:
        return c

class LogViewForm(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        multiTextControl = self.setup_multi_text_control()

        self.btnLogEvents = wx.Button(self, wx.ID_ANY, 'Log')
        self.Bind(wx.EVT_BUTTON, self.onLogEvents, self.btnLogEvents)

        topSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer.Add(self.btnLogEvents, 0, wx.TOP|wx.LEFT, 15)
        topSizer.Add(multiTextControl, 0, wx.ALL|wx.EXPAND, 15)
        self.SetSizer(topSizer)

	pub.subscribe(self.serialListener, 'serialListener')

    def setup_multi_text_control(self):
        headline = 'Log events information\n'
	self.txtMultiCtrl = wx.TextCtrl(self, -1, headline, size=(715, 710), style=wx.TE_MULTILINE)
        self.txtMultiCtrl.SetInsertionPoint(0)

	return self.txtMultiCtrl
	
    def onLogEvents(self, event):
        headline = 60*'-'
	logger.info('Serial port scanned')
        rv = serial_read('log', 4000, self.mySer)
	self.txtMultiCtrl.AppendText(rv + "\n")
	self.txtMultiCtrl.AppendText(headline + "\n")


    def serialListener(self, message, fname=None):
	self.mySer = message

