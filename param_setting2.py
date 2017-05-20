#!/usr/bin/python

# Author      : Heinz Samuelsson
# Date        : ons 10 maj 2017 10:00:55 CEST
# File        : param_setting2.py
# Reference   : -
# Description : Application is used to set parameters for ActSafe's Ascender ACX and TCX.
#               Icons:
#                  http://www.iconarchive.com/show/soft-scraps-icons-by-hopstarter/Button-Play-icon.html
#                  http://www.iconarchive.com/show/colorful-long-shadow-icons-by-graphicloads/Button-eject-icon.html
#
#               Add:
#                     Dialog when exit. Check that motor not is running.
import wx
import time
import serial  

# sizer borders
BORDER1 = 5
BORDER3 = 10
STATIC_BOX_SERIAL_BORDER = 10
STATIC_BOX_PARAMS_BORDER = 5
PARAMSIZER1_BORDER = 2

# color codes
RED     = (255, 0, 0)
GREEN   = (0, 255, 0)
GREY    = (180, 180, 180)
BLACK   = (0, 0, 0)
BROWN   = (200, 160, 100)


def serial_cmd(cmd, serial):
    # send command to serial port
    try:
        serial.write(cmd + '\r');
    except:
        print 'Not Connected!'


class MyForm(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title='Built in Test Tool, Ascender ACX/TCX', size=(900,760))
        self.panel = wx.Panel(self, wx.ID_ANY, style=wx.BORDER_RAISED)

	# flag if function is active
	self.toggle      = False
	self.connected   = False
	self.runningUp   = False
	self.runningDown = False

	# flag to check if parameters have been updated
	self.oldSlKi = 0.25
	self.oldDominantThrottle = 1
	self.oldIqAlpha = 0.005

	self.Centre()
	#self.SetPosition((2500, 480))

	self.load_bitmaps()          # images for up/down/stop buttons 
	self.defineCombo()           # combo box for port names
	self.define_buttons()
	self.define_spin_control()   # spin control for motor speed

        self.txtSerialPort = wx.StaticText(self.panel, wx.ID_ANY, 'Select serial port')

	# Ascender parameters
	self.define_parameters()
	self.define_textctrl_parameters()
	self.disable_txt_controls()

        self.create_sizer1()  # param sizer 1st column
        self.create_sizer2()  # param sizer 2nd column
        self.create_sizer3()  # sizer for Test Enhanced Measuring
        self.create_sizer4()  # param sizer 3rd column

        self.bind_buttons()

	self.statBoxSerial = wx.StaticBox(self.panel, wx.ID_ANY, '  Serial connection    ', size=(0,10))
	self.statBoxSerial.SetBackgroundColour(GREY)
	self.statBoxSerial.SetForegroundColour(BLACK)
        self.staticBoxSizer1 = wx.StaticBoxSizer(self.statBoxSerial, wx.HORIZONTAL)
	self.leftSizer = wx.BoxSizer(wx.HORIZONTAL)
	self.rightSizer = wx.BoxSizer(wx.HORIZONTAL)
	self.leftSizer.Add(self.txtSerialPort, 0, wx.LEFT, STATIC_BOX_SERIAL_BORDER)
	self.leftSizer.Add(self.combo, 0, wx.LEFT, STATIC_BOX_SERIAL_BORDER)
	self.leftSizer.Add(self.btnConnected, 0, wx.LEFT, STATIC_BOX_SERIAL_BORDER)
	self.leftSizer.Add(self.lblConnected, 0, wx.LEFT, STATIC_BOX_SERIAL_BORDER)
	self.rightSizer.Add(self.btnQuit, 0, wx.LEFT, 210)
        self.staticBoxSizer1.Add(self.leftSizer, 0, wx.ALL, STATIC_BOX_SERIAL_BORDER)
        self.staticBoxSizer1.Add(self.rightSizer, 0, wx.ALL, STATIC_BOX_SERIAL_BORDER)

	self.statBoxParams = wx.StaticBox(self.panel, wx.ID_ANY, '  Set parameters   ')
	self.statBoxParams.SetBackgroundColour(GREY)
	self.statBoxParams.SetForegroundColour(BLACK)
        self.staticBoxSizer2 = wx.StaticBoxSizer(self.statBoxParams, wx.HORIZONTAL)
	self.staticBoxSizer2.Add(self.paramSizer1, 0, wx.ALL, STATIC_BOX_PARAMS_BORDER)
	self.staticBoxSizer2.Add(self.paramSizer2, 0, wx.ALL, STATIC_BOX_PARAMS_BORDER)
	self.staticBoxSizer2.Add(self.paramSizer4, 0, wx.ALL, STATIC_BOX_PARAMS_BORDER)

	self.statBoxEnhMeas = wx.StaticBox(self.panel, wx.ID_ANY, '  Test Enhanced Measuring   ')
	self.statBoxEnhMeas.SetBackgroundColour(GREY)
	self.statBoxEnhMeas.SetForegroundColour(BLACK)
	self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
	self.buttonSizer.Add(self.btnConfig2, 0, wx.ALL, 5)
	self.buttonSizer.Add(self.btnTestInject, 0, wx.ALL, 5)
	self.buttonSizer.Add(self.btnGetIq, 0, wx.ALL, 5)
        self.staticBoxSizer3 = wx.StaticBoxSizer(self.statBoxEnhMeas, wx.VERTICAL)
	self.staticBoxSizer3.Add(self.paramSizer3, 1, wx.ALL, 5)
	self.staticBoxSizer3.Add(self.buttonSizer, 1, wx.LEFT, 5)

	self.debuggingSizer = wx.BoxSizer(wx.VERTICAL)
        self.debuggingSizer.Add(self.btnTestRunUp, 0, wx.ALL|wx.EXPAND, BORDER1)
        self.debuggingSizer.Add(self.btnTestRunDown, 0, wx.ALL|wx.EXPAND, BORDER1)

        self.spinnerSizer = wx.BoxSizer(wx.VERTICAL)
	self.spinnerSizer.Add(self.lblSpinCtrl, 0, wx.TOP, 5)
	self.spinnerSizer.Add(self.scSpeed, 0, wx.TOP, 5)

	self.statBoxTestRun = wx.StaticBox(self.panel, wx.ID_ANY, '  Test Run   ')
	self.statBoxTestRun.SetBackgroundColour(GREY)
	self.statBoxTestRun.SetForegroundColour(BLACK)
        self.staticBoxSizer4 = wx.StaticBoxSizer(self.statBoxTestRun, wx.HORIZONTAL)
	self.staticBoxSizer4.Add(self.spinnerSizer, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 15)
	self.staticBoxSizer4.Add(self.debuggingSizer, 0, wx.ALL, BORDER1)
	self.staticBoxSizer4.Add(self.btnTestStop, 0, wx.TOP|wx.BOTTOM, 35)

        self.topSizer = wx.BoxSizer(wx.VERTICAL)
        self.topSizer.Add(self.staticBoxSizer1, 0, wx.ALL|wx.EXPAND, BORDER1)
        self.topSizer.Add(self.staticBoxSizer2, 1, wx.ALL|wx.EXPAND, BORDER1)
        self.topSizer.Add(self.staticBoxSizer3, 1, wx.ALL|wx.EXPAND, BORDER1)
        self.topSizer.Add(self.staticBoxSizer4, 1, wx.ALL|wx.EXPAND, BORDER1)

        self.panel.SetSizer(self.topSizer)

    def load_bitmaps(self):
	self.bmpUp = wx.Bitmap("up.png", wx.BITMAP_TYPE_ANY)
	self.bmpDown = wx.Bitmap("up2.png", wx.BITMAP_TYPE_ANY)
	self.bmpStop = wx.Bitmap("stop.png", wx.BITMAP_TYPE_ANY)
    
    def define_buttons(self):
        self.btnConnected = wx.Button(self.panel, wx.ID_ANY, 'Connect')
	self.lblConnected = wx.StaticText(self.panel, label= 'Not connected                                 ')
        self.btnConfig = wx.Button(self.panel, wx.ID_ANY, 'Configure parameter')
        self.btnTestInject = wx.Button(self.panel, wx.ID_ANY, 'Test Inject')
	self.btnTestInject.SetBackgroundColour(BROWN)
        self.btnGetIq = wx.Button(self.panel, wx.ID_ANY, 'get_iq')
        self.btnQuit = wx.Button(self.panel, wx.ID_ANY, 'Quit')
        self.btnTestRunUp = wx.BitmapButton(self.panel, wx.ID_ANY, bitmap=self.bmpUp)
        self.btnTestRunDown = wx.BitmapButton(self.panel, wx.ID_ANY, bitmap=self.bmpDown)
        self.btnTestStop = wx.BitmapButton(self.panel, wx.ID_ANY, bitmap=self.bmpStop)
        self.btnConfig2 = wx.Button(self.panel, wx.ID_ANY, 'Configure parameter')

    def define_spin_control(self):
	self.scSpeed = wx.SpinCtrl(self.panel, value='0')
	self.scSpeed.SetRange(0, 25)
        self.lblSpinCtrl = wx.StaticText(self.panel, wx.ID_ANY, 'Speed')

    def define_parameters(self):
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

    def define_textctrl_parameters(self):
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

    def create_sizer1(self):
	self.paramSizer1 = wx.BoxSizer(wx.VERTICAL)
	self.paramSizer1.Add(self.param_cl_kp, 0, wx.ALL, PARAMSIZER1_BORDER)
	self.paramSizer1.Add(self.txtCtrl_cl_kp, 0, wx.ALL, PARAMSIZER1_BORDER)
	self.paramSizer1.Add(self.param_cl_ki, 0, wx.ALL, PARAMSIZER1_BORDER)
	self.paramSizer1.Add(self.txtCtrl_cl_ki, 0, wx.ALL, PARAMSIZER1_BORDER)
	self.paramSizer1.Add(self.param_sl_kp, 0, wx.ALL, PARAMSIZER1_BORDER)
	self.paramSizer1.Add(self.txtCtrl_sl_kp, 0, wx.ALL, PARAMSIZER1_BORDER)
	self.paramSizer1.Add(self.param_sl_ki, 0, wx.ALL, PARAMSIZER1_BORDER)
	self.paramSizer1.Add(self.txtCtrl_sl_ki, 0, wx.ALL, PARAMSIZER1_BORDER)
	self.paramSizer1.Add(self.btnConfig, 0, wx.TOP|wx.BOTTOM, PARAMSIZER1_BORDER+10)

    def create_sizer2(self):
	self.paramSizer2 = wx.BoxSizer(wx.VERTICAL)
	self.paramSizer2.Add(self.param_throttle_zero, 0, wx.ALL, BORDER1)
	self.paramSizer2.Add(self.txtCtrl_throttle_zero, 0, wx.ALL, BORDER1)
	self.paramSizer2.Add(self.param_throttle_down, 0, wx.ALL, BORDER1)
	self.paramSizer2.Add(self.txtCtrl_throttle_down, 0, wx.ALL, BORDER1)
	self.paramSizer2.Add(self.param_throttle_up, 0, wx.ALL, BORDER1)
	self.paramSizer2.Add(self.txtCtrl_throttle_up, 0, wx.ALL, BORDER1)
	self.paramSizer2.Add(self.param_throttle_deadband_on, 0, wx.ALL, BORDER1)
	self.paramSizer2.Add(self.txtCtrl_throttle_deadband_on, 0, wx.ALL, BORDER1)

    def create_sizer3(self):
	self.paramSizer3 = wx.BoxSizer(wx.HORIZONTAL)
	self.paramSizer3.Add(self.param_rope_stuck_on, 0, wx.ALL, BORDER1)
	self.paramSizer3.Add(self.txtCtrl_rope_stuck_on, 0, wx.ALL, BORDER1)
	self.paramSizer3.Add(self.param_iq_alpha, 0, wx.ALL, BORDER1)
	self.paramSizer3.Add(self.txtCtrl_iq_alpha, 0, wx.ALL, BORDER1)
	self.paramSizer3.Add(self.param_speed_alpha, 0, wx.ALL, BORDER1)
	self.paramSizer3.Add(self.txtCtrl_speed_alpha, 0, wx.ALL, BORDER1)
	self.paramSizer3.Add(self.param_undershoot, 0, wx.ALL, BORDER1)
	self.paramSizer3.Add(self.txtCtrl_undershoot, 0, wx.ALL, BORDER1)

    def create_sizer4(self):
	self.paramSizer4 = wx.BoxSizer(wx.VERTICAL)
	self.paramSizer4.Add(self.param_par2, 0, wx.ALL, BORDER1)
	self.paramSizer4.Add(self.txtCtrl_par2, 0, wx.ALL, BORDER1)
	self.paramSizer4.Add(self.param_par3, 0, wx.ALL, BORDER1)
	self.paramSizer4.Add(self.txtCtrl_par3, 0, wx.ALL, BORDER1)
	self.paramSizer4.Add(self.param_par4, 0, wx.ALL, BORDER1)
	self.paramSizer4.Add(self.txtCtrl_par4, 0, wx.ALL, BORDER1)
	self.paramSizer4.Add(self.param_dominant_throttle_on, 0, wx.ALL, BORDER1)
	self.paramSizer4.Add(self.txtCtrl_dominant_throttle_on, 0, wx.ALL, BORDER1)

    def bind_buttons(self):
        self.Bind(wx.EVT_BUTTON, self.onConnect, self.btnConnected)
        self.Bind(wx.EVT_BUTTON, self.onTestInject, self.btnTestInject)
        self.Bind(wx.EVT_BUTTON, self.onGetIq, self.btnGetIq)
        self.Bind(wx.EVT_BUTTON, self.onQuit, self.btnQuit)
        self.Bind(wx.EVT_BUTTON, self.onConfig, self.btnConfig)
        self.Bind(wx.EVT_BUTTON, self.onTestRunUp, self.btnTestRunUp)
        self.Bind(wx.EVT_BUTTON, self.onTestRunDown, self.btnTestRunDown)
        self.Bind(wx.EVT_BUTTON, self.onTestStop, self.btnTestStop)
        self.Bind(wx.EVT_BUTTON, self.onConfig, self.btnConfig2)

    def onConnect(self, event):
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
        portNames = ['ACM0', 'ACM1', 'USB0']
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
	self.txtCtrl_par2.Disable()
	self.txtCtrl_par3.Disable()
	self.txtCtrl_par4.Disable()

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

	    # ----------------------------------------------------------------------------------------------------
	    # iq alpha
	    # ----------------------------------------------------------------------------------------------------
            newIqAlpha = int(self.txtCtrl_iq_alpha.GetValue())
	    if (newIqAlpha == self.oldIqAlpha):
		pass
	    else:
                time.sleep(1)
	        # unicode mess ;-)
	        local_cmd = 'param set iq_alpha ' + self.txtCtrl_iq_alpha.GetValue().encode('ascii', 'ignore')
                serial_cmd(local_cmd, self.ser)
	        print 'Updated - iq_alpha = %d' % newIqAlpha
	    self.oldIqAlpha = newIqAlpha

            print 'Config'
	else:
            self.lblConnected.SetForegroundColour(wx.Colour(255,0,0))
	    self.lblConnected.SetLabel('You must connect first!')

    def onTestRunUp(self, event):

        if (self.connected == True):
            self.btnTestRunDown.Enable(False)
            speedValue = self.scSpeed.GetValue()

	    if (self.runningUp == False):
                serial_cmd('e', self.ser)
                time.sleep(1)
                serial_cmd('brake 0', self.ser)
		self.runningUp = True

            time.sleep(1)
            serial_cmd('speed -' + str(speedValue), self.ser)

        else:
            self.lblConnected.SetForegroundColour(wx.Colour(255,0,0))
            self.lblConnected.SetLabel('UP not possible, you must connect first!')

    def onTestRunDown(self, event):

        if (self.connected == True):
            self.btnTestRunUp.Enable(False)
            speedValue = self.scSpeed.GetValue()

	    if (self.runningDown == False):
                serial_cmd('e', self.ser)
                time.sleep(1)
                serial_cmd('brake 0', self.ser)
		self.runningDown = True

            time.sleep(1)
            serial_cmd('speed '+ str(speedValue), self.ser)

        else:
            self.lblConnected.SetForegroundColour(wx.Colour(255,0,0))
            self.lblConnected.SetLabel('DOWN not possible, you must connect first!')

    def onTestStop(self, event):
        print 'Stop'
	serial_cmd('speed 0', self.ser)
        time.sleep(1)
	serial_cmd('d', self.ser)
        time.sleep(1)
	serial_cmd('brake 1', self.ser)
	self.btnTestRunUp.Enable(True)
	self.btnTestRunDown.Enable(True)
	self.runningUp = False
        self.runningDown = False

    def onTestInject(self, event):
	if (self.toggle == False):
	    try:
                serial_cmd('param set ti 1', self.ser)
	        self.btnTestInject.SetBackgroundColour(RED)
	        self.toggle = True
	    except:
                self.lblConnected.SetForegroundColour(wx.Colour(255,0,0))
	        self.lblConnected.SetLabel('You must connect first!')

	else:
	    try:
                serial_cmd('param set ti 0', self.ser)
	        self.btnTestInject.SetBackgroundColour(BROWN)
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
