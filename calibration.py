import wx
import logging
from wx.lib.pubsub import pub
from wx.lib.pubsub import setupkwargs
# Add text 'remember to save par after calib'

RED   = (255, 19, 32)
GREEN = (36, 119, 62)
GREY  = (180, 180, 180)
BLACK = (0, 0, 0)

def serial_cmd(cmd, serial):
    # send command to serial port
    try:
        serial.write(cmd + '\r');
    except:
        print 'Not Connected!'


class CalibForm(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
	alignSizer = self.setup_alignment_sizer()
	calibSizer = self.setup_calibration_sizer()
	saveParamSizer = self.setup_save_param_sizer()

	nullSizer = wx.BoxSizer(wx.VERTICAL)
        txtNull = wx.StaticText(self, wx.ID_ANY, ' ')
	nullSizer.Add(txtNull, 0, wx.TOP, 10)

	nullSizer2 = wx.BoxSizer(wx.VERTICAL)
        txtNull2 = wx.StaticText(self, wx.ID_ANY, ' ')
	nullSizer2.Add(txtNull2, 0, wx.TOP, 10)

        topSizer = wx.BoxSizer(wx.VERTICAL)
	topSizer.Add(alignSizer, 0, wx.TOP|wx.LEFT, 10)
	topSizer.Add(nullSizer, 0, wx.TOP|wx.LEFT, 10)
	topSizer.Add(calibSizer, 0, wx.TOP|wx.LEFT, 10)
	topSizer.Add(nullSizer2, 0, wx.TOP|wx.LEFT, 10)
	topSizer.Add(saveParamSizer, 0, wx.TOP|wx.LEFT, 10)
        self.SetSizer(topSizer)

	pub.subscribe(self.serialListener, 'serialListener')
        logging.basicConfig(format="%(funcName)s() - %(message)s", level=logging.INFO)

    def serialListener(self, message, fname=None):
        print 'msg:', message
	self.mySer = message

    def setup_alignment_sizer(self):
	statBoxSerial = wx.StaticBox(self, wx.ID_ANY, '  Alignment')
	statBoxSerial.SetBackgroundColour(GREY)
	statBoxSerial.SetForegroundColour(BLACK)
        statBoxSizer = wx.StaticBoxSizer(statBoxSerial, wx.HORIZONTAL)

        txtAlignment = wx.StaticText(self, wx.ID_ANY, 'Alignment not performed')
        txtNull = wx.StaticText(self, wx.ID_ANY, ' ')

        btnAlign = wx.Button(self, wx.ID_ANY, 'Align')
        self.Bind(wx.EVT_BUTTON, self.onAlign, btnAlign)

        statBoxSizer.Add(btnAlign, 0, wx.ALL, 20)
        statBoxSizer.Add(txtAlignment, 0, wx.TOP|wx.LEFT|wx.RIGHT, 25)
        statBoxSizer.Add(txtNull, 0, wx.LEFT, 650) # this is just to get the statBoxSerial larger 

	return statBoxSizer

    def setup_calibration_sizer(self):
	statBoxSerial = wx.StaticBox(self, wx.ID_ANY, '  Calibration')
	statBoxSerial.SetBackgroundColour(GREY)
	statBoxSerial.SetForegroundColour(BLACK)
        statBoxSizer = wx.StaticBoxSizer(statBoxSerial, wx.VERTICAL)

        self.txtThrottleMaxUp = wx.StaticText(self, wx.ID_ANY, 'Turn throttle handle max up')
        self.txtThrottleMaxDown = wx.StaticText(self, wx.ID_ANY, 'Turn throttle handle max down')
        self.txtThrottleNeutral = wx.StaticText(self, wx.ID_ANY, 'Set throttle handle in neutal position')
        txtNull = wx.StaticText(self, wx.ID_ANY, ' ')

        self.btnCalibRight = wx.Button(self, wx.ID_ANY, 'Calib Right')
        self.btnCalibLeft = wx.Button(self, wx.ID_ANY, 'Calib Left')
        self.btnCalibNeutral = wx.Button(self, wx.ID_ANY, 'Calib Neutral')
        self.btnCalibRestart = wx.Button(self, wx.ID_ANY, 'Calib Restart')

        self.Bind(wx.EVT_BUTTON, self.onCalibRight, self.btnCalibRight)
        self.Bind(wx.EVT_BUTTON, self.onCalibLeft, self.btnCalibLeft)
        self.Bind(wx.EVT_BUTTON, self.onCalibNeutral, self.btnCalibNeutral)
        self.Bind(wx.EVT_BUTTON, self.onCalibRestart, self.btnCalibRestart)

	self.btnCalibLeft.Enable(False)
	self.btnCalibNeutral.Enable(False)

	rightSizer = wx.BoxSizer(wx.HORIZONTAL)
        rightSizer.Add(self.btnCalibRight, 0, wx.TOP|wx.LEFT, 10)
        rightSizer.Add(self.txtThrottleMaxUp, 0, wx.TOP|wx.LEFT, 15)

	leftSizer = wx.BoxSizer(wx.HORIZONTAL)
        leftSizer.Add(self.btnCalibLeft, 0, wx.TOP|wx.LEFT, 10)
        leftSizer.Add(self.txtThrottleMaxDown, 0, wx.TOP|wx.LEFT, 15)

	neutralSizer = wx.BoxSizer(wx.HORIZONTAL)
        neutralSizer.Add(self.btnCalibNeutral, 0, wx.TOP|wx.LEFT, 10)
        neutralSizer.Add(self.txtThrottleNeutral, 0, wx.TOP|wx.LEFT, 15)

        statBoxSizer.Add(rightSizer, 0, wx.ALL, 10)
        statBoxSizer.Add(leftSizer, 0, wx.ALL, 10)
        statBoxSizer.Add(neutralSizer, 0, wx.ALL, 10)
        statBoxSizer.Add(self.btnCalibRestart, 0, wx.TOP|wx.LEFT, 20)
        statBoxSizer.Add(txtNull, 0, wx.LEFT, 1000) # this is just to get the statBoxSerial larger 

	return statBoxSizer

    def setup_save_param_sizer(self):
	statBoxSerial = wx.StaticBox(self, wx.ID_ANY, '  Save Parameter')
	statBoxSerial.SetBackgroundColour(GREY)
	statBoxSerial.SetForegroundColour(BLACK)
        statBoxSizer = wx.StaticBoxSizer(statBoxSerial, wx.HORIZONTAL)
        txtNull = wx.StaticText(self, wx.ID_ANY, ' ')

        self.txtAlertUser = wx.StaticText(self, wx.ID_ANY, 'Remember ...')

        btnSaveParam = wx.Button(self, wx.ID_ANY, 'Save Param')
        statBoxSizer.Add(btnSaveParam, 0, wx.ALL, 20)
        statBoxSizer.Add(self.txtAlertUser, 0, wx.ALL, 20)
        statBoxSizer.Add(txtNull, 0, wx.LEFT, 870) # this is just to get the statBoxSerial larger 

	return statBoxSizer

    def onAlign(self, event):
        logging.info('')
        serial_cmd('align', self.mySer)

    def onCalibRight(self, event):
        print 'Calib Right'
	self.btnCalibRight.Enable(False)
	self.btnCalibLeft.Enable(True)
	self.txtThrottleMaxUp.SetForegroundColour(GREEN)
	self.txtThrottleMaxUp.SetLabel("Up Calibration finished")

    def onCalibLeft(self, event):
        print 'Calib Left'
	self.btnCalibLeft.Enable(False)
	self.btnCalibNeutral.Enable(True)
	self.txtThrottleMaxDown.SetForegroundColour(GREEN)
	self.txtThrottleMaxDown.SetLabel("Down Calibration finished")

    def onCalibNeutral(self, event):
        print 'Calib Neutral'
	self.btnCalibNeutral.Enable(False)
	self.txtThrottleNeutral.SetForegroundColour(GREEN)
	self.txtThrottleNeutral.SetLabel("Down Calibration finished")
	self.txtAlertUser.SetForegroundColour(RED)
	self.txtAlertUser.SetLabel("Remember to save calibration result")

    def onCalibRestart(self, event):
        print 'Calib Restart'
	self.txtThrottleMaxUp.SetForegroundColour(BLACK)
	self.txtThrottleMaxUp.SetLabel("Turn throttle handle max up")
	self.txtThrottleMaxDown.SetForegroundColour(BLACK)
	self.txtThrottleMaxDown.SetLabel("Turn throttle handle max down")
	self.txtThrottleNeutral.SetForegroundColour(BLACK)
	self.txtThrottleNeutral.SetLabel("Set throttle handle in neutal position")
	self.btnCalibRight.Enable(True)

