import wx
import logging
import datetime
import threading
import time
from wx.lib.pubsub import pub
from wx.lib.pubsub import setupkwargs

RED   = (255, 19, 32)
GREEN = (36, 119, 62)
GREY  = (180, 180, 180)
BLACK = (0, 0, 0)

def serial_cmd(cmd, serial):
    # send command to serial port
    try:
        serial.write(cmd + '\r');
    except:
        logging.info('Not connected')


class PollAlignment(threading.Thread):

    def __init__(self, serial):
        threading.Thread.__init__(self)
	self.ser = serial
        self.start()    # start the thread
 
    def run(self):
        time.sleep(1)
	line = []

        while True:
            for c in self.ser.read():
                line.append(c)
		print 'c:', c
                if (c == 'A'):
		    print 'Now we got Aligned'
		    #s = [''.join(line[:])]
		    #t = s[0]
		    #print 's,t:', s, t
                    #print t[:-2]
                    #line = []
                    wx.CallAfter(pub.sendMessage, topic="topic_aligned", msg="Alignment done", fname=99)
                    #wx.CallAfter(pub.sendMessage, "topic_aligned")
                    #pub.sendMessage('topic_aligned', msg="Alignment done", fname=99)
                    break


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

	self.btnSaveParam.Enable(False) # disabel save param button from beginning, enabled after last calibration

	pub.subscribe(self.serialListener, 'serialListener')
        logging.basicConfig(format="%(filename)s: %(funcName)s() - %(message)s", level=logging.INFO)

    def serialListener(self, message, fname=None):
        print 'msg:', message
	self.mySer = message

    def setup_alignment_sizer(self):
	statBoxSerial = wx.StaticBox(self, wx.ID_ANY, '  Alignment')
	statBoxSerial.SetBackgroundColour(GREY)
	statBoxSerial.SetForegroundColour(BLACK)
        statBoxSizer = wx.StaticBoxSizer(statBoxSerial, wx.HORIZONTAL)

        self.txtAlignment = wx.StaticText(self, wx.ID_ANY, 'Alignment not performed')
        txtNull = wx.StaticText(self, wx.ID_ANY, ' ')

        self.btnAlign = wx.Button(self, wx.ID_ANY, 'Align')
        self.Bind(wx.EVT_BUTTON, self.onAlign, self.btnAlign)

        statBoxSizer.Add(self.btnAlign, 0, wx.ALL, 20)
        statBoxSizer.Add(self.txtAlignment, 0, wx.TOP|wx.LEFT|wx.RIGHT, 25)
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

        self.Bind(wx.EVT_BUTTON, self.onCalibUp, self.btnCalibRight)
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

	pub.subscribe(self.aligned_finished, "topic_aligned")

	return statBoxSizer

    def setup_save_param_sizer(self):
	statBoxSerial = wx.StaticBox(self, wx.ID_ANY, '  Save Parameter')
	statBoxSerial.SetBackgroundColour(GREY)
	statBoxSerial.SetForegroundColour(BLACK)
        statBoxSizer = wx.StaticBoxSizer(statBoxSerial, wx.HORIZONTAL)
        txtNull = wx.StaticText(self, wx.ID_ANY, ' ')

        self.txtAlertUser = wx.StaticText(self, wx.ID_ANY, '...')

        self.btnSaveParam = wx.Button(self, wx.ID_ANY, 'Save Param')
        self.Bind(wx.EVT_BUTTON, self.onSaveParam, self.btnSaveParam)
        statBoxSizer.Add(self.btnSaveParam, 0, wx.ALL, 20)
        statBoxSizer.Add(self.txtAlertUser, 0, wx.ALL, 20)
        statBoxSizer.Add(txtNull, 0, wx.LEFT, 830) # this is just to get the statBoxSerial larger 

	return statBoxSizer

    def onAlign(self, event):
        logging.info('')

	# poll answer from Ascender when alignment is done
	PollAlignment(self.mySer)

	self.txtAlignment.SetForegroundColour(RED)
	self.txtAlignment.SetLabel("Alignment initiated")
	self.btnSaveParam.Enable(True)
	self.operation = 'alignment'
        serial_cmd('align', self.mySer)

    def onCalibUp(self, event):
        logging.info('Calibration Up done')
	self.btnSaveParam.Enable(False)
	self.btnCalibRight.Enable(False)
	self.btnCalibLeft.Enable(True)
	self.txtThrottleMaxUp.SetForegroundColour(GREEN)
	self.txtThrottleMaxUp.SetLabel("Up Calibration finished")
        serial_cmd('throttle cal 1', self.mySer)

    def onCalibLeft(self, event):
        logging.info('Calibration Down done')
	self.btnCalibLeft.Enable(False)
	self.btnCalibNeutral.Enable(True)
	self.txtThrottleMaxDown.SetForegroundColour(GREEN)
	self.txtThrottleMaxDown.SetLabel("Down Calibration finished")
        serial_cmd('throttle cal -1', self.mySer)

    def onCalibNeutral(self, event):
        logging.info('Calibration Neutral done')
	self.btnCalibNeutral.Enable(False)
	self.txtThrottleNeutral.SetForegroundColour(GREEN)
	self.txtThrottleNeutral.SetLabel("Down Calibration finished")
	self.txtAlertUser.SetForegroundColour(RED)
	self.txtAlertUser.SetLabel("Remember to save calibration result")
	self.operation = 'calibration'
        serial_cmd('throttle cal 0', self.mySer)
	self.btnSaveParam.Enable(True)

    def onCalibRestart(self, event):
        logging.info('Calibration Restarted')
	self.txtThrottleMaxUp.SetForegroundColour(BLACK)
	self.txtThrottleMaxUp.SetLabel("Turn throttle handle max up")
	self.txtThrottleMaxDown.SetForegroundColour(BLACK)
	self.txtThrottleMaxDown.SetLabel("Turn throttle handle max down")
	self.txtThrottleNeutral.SetForegroundColour(BLACK)
	self.txtThrottleNeutral.SetLabel("Set throttle handle in neutal position")
	self.btnCalibRight.Enable(True)
	self.btnSaveParam.Enable(False)
	self.txtAlertUser.SetLabel(" ")

    def onSaveParam(self, event):
        logging.info('Save configuration after calibration')
	now = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M")
	self.txtAlertUser.SetForegroundColour(GREEN)
	self.txtAlertUser.SetLabel("Parameter saved after " + self.operation + " at  " + str(now))
        serial_cmd('save param', self.mySer)

    def aligned_finished(self, msg, fname=None):
        logging.info('')
	self.btnAlign.Enable(True)
	self.txtAlignment.SetForegroundColour(GREEN)
	self.txtAlignment.SetLabel("Alignment finished.")
	self.btnCalibRight.Enable(True)
	self.btnCalibRestart.Enable(True)

	#t = 21
        ##t = msg.data
	#print msg

	#if isinstance(t, int):
	#    print 't:', t
	#else:
	#    print 'else', t
	#    self.btnAlign.Enable(True)
	#    self.txtAlignment.SetForegroundColour(GREEN)
	#    self.txtAlignment.SetLabel("Alignment finished.")
	#    self.btnCalibRight.Enable(True)
	#    self.btnCalibRestart.Enable(True)

