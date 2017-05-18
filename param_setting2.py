#!/usr/bin/python

# Author      : Heinz Samuelsson
# Date        : ons 10 maj 2017 10:00:55 CEST
# File        : param_setting2.py
# Reference   : -
# Description : Application is used to set parameters for ActSafe's Ascender ACX and TCX.
#               Icons:
#                  http://www.iconarchive.com/show/soft-scraps-icons-by-hopstarter/Button-Play-icon.html
#                  http://www.iconarchive.com/show/colorful-long-shadow-icons-by-graphicloads/Button-eject-icon.html
import wx
import time
import serial  

BORDER1 = 5
BORDER2 = 15
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (180, 180, 180)
BLACK = (0, 0, 0)
INJECT_COLOR = (200, 160, 100)


def serial_cmd(cmd, serial):
    # send command to serial port
    try:
        serial.write(cmd + '\r');
    except:
        print 'Not Connected!'


class MyForm(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title='Parameter Setting', size=(900,685))
        self.panel = wx.Panel(self, wx.ID_ANY, style=wx.BORDER_RAISED)

	self.toggle      = False
	self.connected   = False
	self.downRunning = False
	self.upRunning   = False
	self.testPort    = False
	self.oldSlKi = 0.25
	self.oldDominantThrottle = 1

	self.Centre()
	#self.SetPosition((2500, 480))

	bmpUp = wx.Bitmap("up.png", wx.BITMAP_TYPE_ANY)
	bmpDown = wx.Bitmap("up2.png", wx.BITMAP_TYPE_ANY)
	bmpStop = wx.Bitmap("stop.png", wx.BITMAP_TYPE_ANY)

        self.connectBtn = wx.Button(self.panel, wx.ID_ANY, 'Connect')
	self.lblConnected = wx.StaticText(self.panel, label= 'Not connected                                 ')
        self.configBtn = wx.Button(self.panel, wx.ID_ANY, 'Configure parameter')
        self.testInjectBtn = wx.Button(self.panel, wx.ID_ANY, 'Test Inject')
	self.testInjectBtn.SetBackgroundColour(INJECT_COLOR)
        self.getIqBtn = wx.Button(self.panel, wx.ID_ANY, 'get_iq')
        self.quitBtn = wx.Button(self.panel, wx.ID_ANY, 'Quit')
        self.testRunUpBtn = wx.BitmapButton(self.panel, wx.ID_ANY, bitmap=bmpUp)
        self.testRunDownBtn = wx.BitmapButton(self.panel, wx.ID_ANY, bitmap=bmpDown)
        self.testStopBtn = wx.BitmapButton(self.panel, wx.ID_ANY, bitmap=bmpStop)

	self.defineCombo()

        self.txtSerialPort = wx.StaticText(self.panel, wx.ID_ANY, 'Select serial port')

        self.param_cl_kp = wx.StaticText(self.panel, wx.ID_ANY, 'cl.kp')
        self.param_cl_ki = wx.StaticText(self.panel, wx.ID_ANY, 'cl.ki')
        self.param_sl_kp = wx.StaticText(self.panel, wx.ID_ANY, 'sl.kp')
        self.param_sl_ki = wx.StaticText(self.panel, wx.ID_ANY, 'sl.ki')
        self.param_throttle_zero = wx.StaticText(self.panel, wx.ID_ANY, 'throttle_zero')
        self.param_throttle_down = wx.StaticText(self.panel, wx.ID_ANY, 'throttle_down')
        self.param_throttle_up = wx.StaticText(self.panel, wx.ID_ANY, 'throttle_up')
        self.param_throttle_deadband_on = wx.StaticText(self.panel, wx.ID_ANY, 'throttle_deadband_on')
        self.param_dominant_throttle_on = wx.StaticText(self.panel, wx.ID_ANY, 'dominant_throttle_on')
        self.param_rope_stuck_on = wx.StaticText(self.panel, wx.ID_ANY, 'rope_stuck_on')
        self.param_iq_alpha = wx.StaticText(self.panel, wx.ID_ANY, 'iq_alpha')
        self.param_speed_alpha = wx.StaticText(self.panel, wx.ID_ANY, 'speed_alpha')
        self.param_undershoot = wx.StaticText(self.panel, wx.ID_ANY, 'undershoot')
        self.param_par2 = wx.StaticText(self.panel, wx.ID_ANY, 'par2')
        self.param_par3 = wx.StaticText(self.panel, wx.ID_ANY, 'par3')
        self.param_par4 = wx.StaticText(self.panel, wx.ID_ANY, 'par4')

        self.txtCtrl_cl_kp = wx.TextCtrl(self.panel, wx.ID_ANY,'0.23')
        self.txtCtrl_cl_ki = wx.TextCtrl(self.panel, wx.ID_ANY,'13')
        self.txtCtrl_sl_kp = wx.TextCtrl(self.panel, wx.ID_ANY,'15')
        self.txtCtrl_sl_ki = wx.TextCtrl(self.panel, wx.ID_ANY,'0.25')
        self.txtCtrl_throttle_zero = wx.TextCtrl(self.panel, wx.ID_ANY,'25')
        self.txtCtrl_throttle_down = wx.TextCtrl(self.panel, wx.ID_ANY,'0.5')
        self.txtCtrl_throttle_up = wx.TextCtrl(self.panel, wx.ID_ANY,'4')
        self.txtCtrl_throttle_deadband_on = wx.TextCtrl(self.panel, wx.ID_ANY,'0.25')
        self.txtCtrl_dominant_throttle_on = wx.TextCtrl(self.panel, wx.ID_ANY,'1')
        self.txtCtrl_rope_stuck_on = wx.TextCtrl(self.panel, wx.ID_ANY,'1')
        self.txtCtrl_iq_alpha = wx.TextCtrl(self.panel, wx.ID_ANY,'0.005')
        self.txtCtrl_speed_alpha = wx.TextCtrl(self.panel, wx.ID_ANY,'0.05')
        self.txtCtrl_undershoot = wx.TextCtrl(self.panel, wx.ID_ANY,'-1.0')
        self.txtCtrl_par2 = wx.TextCtrl(self.panel, wx.ID_ANY,'0.6')
        self.txtCtrl_par3 = wx.TextCtrl(self.panel, wx.ID_ANY,'0.05')
        self.txtCtrl_par4 = wx.TextCtrl(self.panel, wx.ID_ANY,'0.3')

	self.disable_txt_controls()

	self.paramSizer1 = wx.BoxSizer(wx.VERTICAL)
	self.paramSizer1.Add(self.param_cl_kp, 0, wx.ALL, BORDER1)
	self.paramSizer1.Add(self.txtCtrl_cl_kp, 0, wx.ALL, BORDER1)
	self.paramSizer1.Add(self.param_cl_ki, 0, wx.ALL, BORDER1)
	self.paramSizer1.Add(self.txtCtrl_cl_ki, 0, wx.ALL, BORDER1)
	self.paramSizer1.Add(self.param_sl_kp, 0, wx.ALL, BORDER1)
	self.paramSizer1.Add(self.txtCtrl_sl_kp, 0, wx.ALL, BORDER1)
	self.paramSizer1.Add(self.param_sl_ki, 0, wx.ALL, BORDER1)
	self.paramSizer1.Add(self.txtCtrl_sl_ki, 0, wx.ALL, BORDER1)
	self.paramSizer1.Add(self.configBtn, 0, wx.TOP|wx.BOTTOM, BORDER2)

	self.paramSizer2 = wx.BoxSizer(wx.VERTICAL)
	self.paramSizer2.Add(self.param_throttle_zero, 0, wx.ALL, BORDER1)
	self.paramSizer2.Add(self.txtCtrl_throttle_zero, 0, wx.ALL, BORDER1)
	self.paramSizer2.Add(self.param_throttle_down, 0, wx.ALL, BORDER1)
	self.paramSizer2.Add(self.txtCtrl_throttle_down, 0, wx.ALL, BORDER1)
	self.paramSizer2.Add(self.param_throttle_up, 0, wx.ALL, BORDER1)
	self.paramSizer2.Add(self.txtCtrl_throttle_up, 0, wx.ALL, BORDER1)
	self.paramSizer2.Add(self.param_throttle_deadband_on, 0, wx.ALL, BORDER1)
	self.paramSizer2.Add(self.txtCtrl_throttle_deadband_on, 0, wx.ALL, BORDER1)

	self.paramSizer3 = wx.BoxSizer(wx.VERTICAL)
	self.paramSizer3.Add(self.param_dominant_throttle_on, 0, wx.ALL, BORDER1)
	self.paramSizer3.Add(self.txtCtrl_dominant_throttle_on, 0, wx.ALL, BORDER1)
	self.paramSizer3.Add(self.param_rope_stuck_on, 0, wx.ALL, BORDER1)
	self.paramSizer3.Add(self.txtCtrl_rope_stuck_on, 0, wx.ALL, BORDER1)
	self.paramSizer3.Add(self.param_iq_alpha, 0, wx.ALL, BORDER1)
	self.paramSizer3.Add(self.txtCtrl_iq_alpha, 0, wx.ALL, BORDER1)
	self.paramSizer3.Add(self.param_speed_alpha, 0, wx.ALL, BORDER1)
	self.paramSizer3.Add(self.txtCtrl_speed_alpha, 0, wx.ALL, BORDER1)

	self.paramSizer4 = wx.BoxSizer(wx.VERTICAL)
	self.paramSizer4.Add(self.param_undershoot, 0, wx.ALL, BORDER1)
	self.paramSizer4.Add(self.txtCtrl_undershoot, 0, wx.ALL, BORDER1)
	self.paramSizer4.Add(self.param_par2, 0, wx.ALL, BORDER1)
	self.paramSizer4.Add(self.txtCtrl_par2, 0, wx.ALL, BORDER1)
	self.paramSizer4.Add(self.param_par3, 0, wx.ALL, BORDER1)
	self.paramSizer4.Add(self.txtCtrl_par3, 0, wx.ALL, BORDER1)
	self.paramSizer4.Add(self.param_par4, 0, wx.ALL, BORDER1)
	self.paramSizer4.Add(self.txtCtrl_par4, 0, wx.ALL, BORDER1)

        self.Bind(wx.EVT_BUTTON, self.onConnect, self.connectBtn)
        self.Bind(wx.EVT_BUTTON, self.onTestInject, self.testInjectBtn)
        self.Bind(wx.EVT_BUTTON, self.onGetIq, self.getIqBtn)
        self.Bind(wx.EVT_BUTTON, self.onQuit, self.quitBtn)
        self.Bind(wx.EVT_BUTTON, self.onConfig, self.configBtn)
        self.Bind(wx.EVT_BUTTON, self.onTestRunUp, self.testRunUpBtn)
        self.Bind(wx.EVT_BUTTON, self.onTestRunDown, self.testRunDownBtn)
        self.Bind(wx.EVT_BUTTON, self.onTestStop, self.testStopBtn)

	self.statBoxSerial = wx.StaticBox(self.panel, wx.ID_ANY, '  Serial connection    ', size=(0,20))
	self.statBoxSerial.SetBackgroundColour(GREY)
	self.statBoxSerial.SetForegroundColour(BLACK)
        self.staticBoxSizer1 = wx.StaticBoxSizer(self.statBoxSerial, wx.HORIZONTAL)
        self.staticBoxSizer1.Add(self.txtSerialPort, 0, wx.BOTTOM|wx.TOP|wx.LEFT, BORDER2)
        self.staticBoxSizer1.Add(self.combo, 0, wx.BOTTOM|wx.TOP|wx.LEFT, BORDER2)
	self.staticBoxSizer1.Add(self.connectBtn, 0, wx.BOTTOM|wx.TOP|wx.LEFT, BORDER2)
	self.staticBoxSizer1.Add(self.lblConnected, 0, wx.BOTTOM|wx.TOP|wx.LEFT, BORDER2)
	#self.staticBoxSizer1.Add(self.quitBtn, 0, wx.BOTTOM|wx.TOP|wx.LEFT, BORDER2)
	self.staticBoxSizer1.Add(self.quitBtn, 0, wx.BOTTOM|wx.TOP, BORDER2)

	self.statBoxParams = wx.StaticBox(self.panel, wx.ID_ANY, '  Parameters   ')
	self.statBoxParams.SetBackgroundColour(GREY)
	self.statBoxParams.SetForegroundColour(BLACK)
        self.staticBoxSizer2 = wx.StaticBoxSizer(self.statBoxParams, wx.HORIZONTAL)
	self.staticBoxSizer2.Add(self.paramSizer1, 0, wx.ALL, BORDER1)
	self.staticBoxSizer2.Add(self.paramSizer2, 0, wx.ALL, BORDER1)
	self.staticBoxSizer2.Add(self.paramSizer3, 0, wx.ALL, BORDER1)
	self.staticBoxSizer2.Add(self.paramSizer4, 0, wx.ALL, BORDER1)

	self.statBoxMisc = wx.StaticBox(self.panel, wx.ID_ANY, '  Debugging   ')
	self.statBoxMisc.SetBackgroundColour(GREY)
	self.statBoxMisc.SetForegroundColour(BLACK)
        self.staticBoxSizer3 = wx.StaticBoxSizer(self.statBoxMisc, wx.HORIZONTAL)
	self.staticBoxSizer3.Add(self.testInjectBtn, 0, wx.ALL, BORDER1)
	self.staticBoxSizer3.Add(self.getIqBtn, 0, wx.ALL, BORDER1)

	self.debuggingSizer = wx.BoxSizer(wx.VERTICAL)
        self.debuggingSizer.Add(self.testRunUpBtn, 0, wx.ALL|wx.EXPAND, BORDER1)
        self.debuggingSizer.Add(self.testRunDownBtn, 0, wx.ALL|wx.EXPAND, BORDER1)

	self.statBoxTestRun = wx.StaticBox(self.panel, wx.ID_ANY, '  Test Run   ')
	self.statBoxTestRun.SetBackgroundColour(GREY)
	self.statBoxTestRun.SetForegroundColour(BLACK)
        self.staticBoxSizer4 = wx.StaticBoxSizer(self.statBoxTestRun, wx.HORIZONTAL)
	self.staticBoxSizer4.Add(self.debuggingSizer, 0, wx.ALL, BORDER1)
	self.staticBoxSizer4.Add(self.testStopBtn, 0, wx.TOP|wx.BOTTOM, 35)

        self.topSizer = wx.BoxSizer(wx.VERTICAL)
        self.topSizer.Add(self.staticBoxSizer1, 1, wx.ALL|wx.EXPAND, BORDER1)
        self.topSizer.Add(self.staticBoxSizer2, 1, wx.ALL|wx.EXPAND, BORDER1)
        self.topSizer.Add(self.staticBoxSizer3, 1, wx.ALL|wx.EXPAND, BORDER1)
        self.topSizer.Add(self.staticBoxSizer4, 1, wx.ALL|wx.EXPAND, BORDER1)

        self.panel.SetSizer(self.topSizer)

    def onConnect(self, event):
	if (self.combo.GetValue()):
	    print 'Test port'
	    self.testPort = True
            self.lblConnected.SetForegroundColour(wx.Colour(50, 90 , 150))
            self.lblConnected.SetLabel('Connected to ' + self.combo.GetValue())

	else:
	    try:
	        self.connected = True
                self.ser = serial.Serial(port = '/dev/tty'+self.combo.GetValue(),
                                         baudrate = 9600,
                                         parity = serial.PARITY_NONE,
                                         stopbits = serial.STOPBITS_ONE,
                                         bytesize = serial.EIGHTBITS,
                                         timeout = 1)

                self.lblConnected.SetForegroundColour(wx.Colour(50, 90 , 150))
                self.lblConnected.SetLabel('Connected to tty' + self.combo.GetValue())

	    except:
                self.lblConnected.SetForegroundColour(wx.Colour(255,0,0))
	        self.lblConnected.SetLabel('Cannot connect')

    def defineCombo(self):
        portNames = ['ACM0', 'ACM1', 'USB0', 'TestPort']
        self.combo = wx.ComboBox(self.panel, choices=portNames)
        self.combo.SetSelection(0) # preselect ACM0
        self.combo.Bind(wx.EVT_COMBOBOX, self.onCombo)

    def disable_txt_controls(self):
	self.txtCtrl_cl_kp.Disable()
	self.txtCtrl_cl_ki.Disable()
	self.txtCtrl_sl_kp.Disable()
	self.txtCtrl_throttle_zero.Disable()
	self.txtCtrl_throttle_down.Disable()
	self.txtCtrl_throttle_up.Disable()
	self.txtCtrl_throttle_deadband_on.Disable()
	self.txtCtrl_rope_stuck_on.Disable()
	self.txtCtrl_iq_alpha.Disable()
	self.txtCtrl_speed_alpha.Disable()
	self.txtCtrl_undershoot.Disable()

    def onConfig(self, event):
	if (self.connected == True):
	    # ----------------------------------------------------------------------------------------------------
            # speed loop ki
	    # ----------------------------------------------------------------------------------------------------
            newSlKi = float(self.txtCtrl_sl_ki.GetValue())
	    if (newSlKi == self.oldSlKi):
		pass
	    else:
                time.sleep(1)
	        # unicode mess ;-)
	        local_cmd = 'param set motor.sl.ki ' + self.txtCtrl_sl_ki.GetValue().encode('ascii', 'ignore')
                serial_cmd(local_cmd, self.ser)
	        print 'Updated - sl.ki = %f' % newSlKi
	    self.oldSlKi = newSlKi

	    # ----------------------------------------------------------------------------------------------------
	    # Dominant throttle
	    # ----------------------------------------------------------------------------------------------------
            newDominantThrottle = int(self.txtCtrl_dominant_throttle_on.GetValue())
	    if (newDominantThrottle == self.oldDominantThrottle):
		pass
	    else:
                time.sleep(1)
	        # unicode mess ;-)
	        local_cmd = 'param set dominant_throttle_on ' + self.txtCtrl_dominant_throttle_on.GetValue().encode('ascii', 'ignore')
                serial_cmd(local_cmd, self.ser)
	        print 'Updated - dominant_trottle_on = %d' % newDominantThrottle
	    self.oldDominantThrottle = newDominantThrottle

            print 'Config'
	else:
            self.lblConnected.SetForegroundColour(wx.Colour(255,0,0))
	    self.lblConnected.SetLabel('You must connect first!')

    def onTestRunUp(self, event):
	if (self.testPort == True):
	    self.upRunning = True
	    print 'Up'

	else:
	    if (self.downRunning == True):
	        print 'Already running down. Need to stop'
	    else:
	        try:
	            serial_cmd('e', self.ser)
                    time.sleep(1)
	            serial_cmd('brake 0', self.ser)
                    time.sleep(1)
	            serial_cmd('speed -5', self.ser)
	            self.upRunning = True
	        except:
                    self.lblConnected.SetForegroundColour(wx.Colour(255,0,0))
	            self.lblConnected.SetLabel('You must connect first!')

    def onTestRunDown(self, event):
	if (self.upRunning == True):
	    print 'Already running Up. Need to stop'
	else:
	    try:
	        serial_cmd('e', self.ser)
                time.sleep(1)
	        serial_cmd('brake 0', self.ser)
                time.sleep(1)
	        serial_cmd('speed 5', self.ser)
	        self.downRunning = True
	    except:
                self.lblConnected.SetForegroundColour(wx.Colour(255,0,0))
	        self.lblConnected.SetLabel('You must connect first!')

    def onTestStop(self, event):
	serial_cmd('speed 0', self.ser)
        time.sleep(1)
	serial_cmd('d', self.ser)
        time.sleep(1)
	serial_cmd('brake 1', self.ser)
	self.downRunning = False
	self.upRunning = False

    def onTestInject(self, event):
	if (self.toggle == False):
	    try:
                serial_cmd('param set ti 1', self.ser)
	        self.testInjectBtn.SetBackgroundColour(RED)
	        self.toggle = True
	    except:
                self.lblConnected.SetForegroundColour(wx.Colour(255,0,0))
	        self.lblConnected.SetLabel('You must connect first!')

	else:
	    try:
                serial_cmd('param set ti 0', self.ser)
	        self.testInjectBtn.SetBackgroundColour(INJECT_COLOR)
	        self.toggle = False
	    except:
                self.lblConnected.SetForegroundColour(wx.Colour(255,0,0))
	        self.lblConnected.SetLabel('You must connect first!')


    def onGetIq(self, event):
	try:
	    serial_cmd('get_iq', self.ser)
	except:
            self.lblConnected.SetForegroundColour(wx.Colour(255,0,0))
	    self.lblConnected.SetLabel('You must connect first!')

    def onCombo(self, event):
        print 'Selected port: ' + self.combo.GetValue()

    def onQuit(self, event):
        self.Close()


if __name__ == '__main__':
    app = wx.App()
    frame = MyForm().Show()
    app.MainLoop()
