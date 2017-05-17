#!/usr/bin/python
# Author      : Heinz Samuelsson
# Date        : ons 10 maj 2017 10:00:55 CEST
# File        : param_setting.py
# Reference   : -
# Description : Application is used to set parameters for ActSafe's
#               Ascender ACX and TCX.
#
#
#   +--------------------------------------------------------------------------------------+
#   |  topSizer                                                                            |
#   |                                                                                      |
#   |   +------------------------------------------------------------------------------+   |
#   |   | infoSizer                                                                    |   |
#   |   |                                                                              |   |
#   |   +------------------------------------------------------------------------------+   |
#   |                                                                                      |
#   | +----------------------------------------------------------------------------------+ |
#   | | paramTopSizer                                                                    | |
#   | |                                                                                  | |
#   | | +-------------------------------------+  +-------------------------------------+ | |
#   | | |  paramSizer1                        |  |  paramSizer2                        | | |
#   | | |                                     |  |                                     | | |
#   | | |   +------------+   +-------------+  |  |   +------------+   +-------------+  | | |
#   | | |   | leftSizer1 |   | rightSizer1 |  |  |   | leftSizer2 |   | rightSizer2 |  | | |
#   | | |   |            |   |             |  |  |   |            |   |             |  | | |
#   | | |   +------------+   +-------------+  |  |   +------------+   +-------------+  | | |
#   | | |                                     |  |                                     | | |
#   | | +-------------------------------------+  +-------------------------------------+ | |
#   | |                                                                                  | |
#   | +----------------------------------------------------------------------------------+ |
#   |                                                                                      |
#   |   +------------------------------------------------------------------------------+   |
#   |   | buttonSizer                                                                  |   |
#   |   |                                                                              |   |
#   |   +------------------------------------------------------------------------------+   |
#   |                                                                                      |
#   +-------------------------------------------------------------------------------------+
#

import serial
import wx
import time

BORDER1 = 8
BORDER2 = 3
GREEN = (0, 255, 0)
INJECT_COLOR = (200, 160, 100)

def serial_cmd(cmd, serial):
    # send command to serial port
    try:
        serial.write(cmd + '\r');
    except:
        print 'Not Connected!'


class MyForm(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title='ACX/TCX Parameter Setting Tool')
	self.oldClKp = 0.23
	self.oldClKi = 0.03
	self.oldSlKi = 0.25
	self.oldDominantThrottle = 1
	self.oldRope_stuck_on    = 1
	self.oldIqAlpha = 0.005
	self.toggle  = False
	self.connected = False

        self.panel = wx.Panel(self, wx.ID_ANY, style=wx.RAISED_BORDER)

	# get screen size, not used at the moment
	w = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
        h = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)

	#self.Centre()
	self.SetPosition((2500, 480))

	self.lblConnected = wx.StaticText(self.panel, label= 'Not connected')
	self.lblConnected.SetForegroundColour(wx.Colour(255, 0 , 255))

        connectBtn = wx.Button(self.panel, wx.ID_ANY, 'Connect')
        updateBtn = wx.Button(self.panel, wx.ID_ANY, 'Update')
        self.testInjectBtn = wx.Button(self.panel, wx.ID_ANY, 'Test Inject')
        quitBtn = wx.Button(self.panel, wx.ID_ANY, 'Quit')
	self.testInjectBtn.SetBackgroundColour(INJECT_COLOR)
        self.getIqBtn = wx.Button(self.panel, wx.ID_ANY, 'get_iq')

        self.Bind(wx.EVT_BUTTON, self.onConnect, connectBtn)
        self.Bind(wx.EVT_BUTTON, self.onUpdate, updateBtn)
        self.Bind(wx.EVT_BUTTON, self.onTestInject, self.testInjectBtn)
        self.Bind(wx.EVT_BUTTON, self.onGetIq, self.getIqBtn)
        self.Bind(wx.EVT_BUTTON, self.onQuit, quitBtn)

	self.defineCombo()

	self.define_sizers()
	self.define_static_text()
	self.define_textctrl()
	self.define_left_sizer()
	self.define_right_sizer()

	self.disable_txt_controls()

        self.infoSizer.Add(self.combo, 1, wx.ALL|wx.CENTER, BORDER2)
        self.infoSizer.Add(connectBtn, 1, wx.ALL|wx.CENTER, BORDER2)
        self.infoSizer.Add(self.lblConnected, 1, wx.ALL|wx.CENTER, BORDER2)
        self.infoSizer.Add((0,0), proportion=1, flag=wx.EXPAND)

        self.buttonSizer.Add(updateBtn, 1, wx.ALL, BORDER1)
        self.buttonSizer.Add(self.testInjectBtn, 1, wx.ALL, BORDER1)
        self.buttonSizer.Add(self.getIqBtn, 1, wx.ALL, BORDER1)
        self.buttonSizer.Add((0,0), proportion=4, flag=wx.EXPAND)
        self.buttonSizer.Add(quitBtn, 1, wx.ALL, BORDER1)

	self.paramSizer1.Add(self.leftSizer1, 0, wx.ALL, BORDER2)
	self.paramSizer1.Add(self.rightSizer1, 0, wx.ALL, BORDER2)
	self.paramSizer2.Add(self.leftSizer2, 0, wx.ALL, BORDER2)
	self.paramSizer2.Add(self.rightSizer2, 0, wx.ALL, BORDER2)
	self.paramSizer3.Add(self.leftSizer3, 0, wx.ALL, BORDER2)
	self.paramSizer3.Add(self.rightSizer3, 0, wx.ALL, BORDER2)

	self.paramTopSizer.Add(self.paramSizer1, 0, wx.ALL, BORDER2)
	self.paramTopSizer.Add(self.paramSizer2, 0, wx.ALL, BORDER2)
	self.paramTopSizer.Add(self.paramSizer3, 0, wx.ALL, BORDER2)

        self.topSizer.Add(self.infoSizer, 0, wx.ALL, 5)
        self.topSizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, BORDER2)
        self.topSizer.Add(self.paramTopSizer, 0, wx.ALL, 5)
        self.topSizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, BORDER2)
        self.topSizer.Add(self.buttonSizer, 0, wx.ALL, 5)

        self.panel.SetSizer(self.topSizer)
        self.topSizer.Fit(self)

    def defineCombo(self):
        portNames = ['ACM0', 'ACM1', 'USB0']
        self.combo = wx.ComboBox(self.panel, choices=portNames, pos=(140, 27))
        self.combo.SetSelection(0) # preselect ACM0
        self.combo.Bind(wx.EVT_COMBOBOX, self.onCombo)
    
    def disable_txt_controls(self):
	self.txtCtrl_cl_kp.Disable()
	self.txtCtrl_cl_ki.Disable()
	self.txtCtrl_sl_kp.Disable()
	self.txtCtrl_sl_kt.Disable()
	self.txtCtrl_throttle_zero.Disable()
	self.txtCtrl_throttle_down.Disable()
	self.txtCtrl_throttle_up.Disable()
	self.txtCtrl_throttle_deadband_on.Disable()
        self.txtCtrl_speed_alpha.Disable()

    def define_sizers(self):
        self.topSizer       = wx.BoxSizer(wx.VERTICAL)
        self.paramTopSizer  = wx.BoxSizer(wx.HORIZONTAL)
        self.infoSizer      = wx.BoxSizer(wx.HORIZONTAL)

	self.paramSizer1    = wx.BoxSizer(wx.HORIZONTAL)
        self.leftSizer1     = wx.BoxSizer(wx.VERTICAL)
        self.rightSizer1    = wx.BoxSizer(wx.VERTICAL)

	self.paramSizer2    = wx.BoxSizer(wx.HORIZONTAL)
        self.leftSizer2     = wx.BoxSizer(wx.VERTICAL)
        self.rightSizer2    = wx.BoxSizer(wx.VERTICAL)

	self.paramSizer3    = wx.BoxSizer(wx.HORIZONTAL)
        self.leftSizer3     = wx.BoxSizer(wx.VERTICAL)
        self.rightSizer3    = wx.BoxSizer(wx.VERTICAL)

        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

    def define_static_text(self):
        self.param_cl_kp = wx.StaticText(self.panel, wx.ID_ANY, 'param.cl.kp')
        self.param_cl_ki = wx.StaticText(self.panel, wx.ID_ANY, 'param.cl.ki')
        self.param_sl_kp = wx.StaticText(self.panel, wx.ID_ANY, 'param.sl.kp')
        self.param_sl_ki = wx.StaticText(self.panel, wx.ID_ANY, 'param.sl.ki')
        self.param_sl_kt = wx.StaticText(self.panel, wx.ID_ANY, 'param.sl.kt')

        self.param_throttle_zero = wx.StaticText(self.panel, wx.ID_ANY, 'param.throttle_zero')
        self.param_throttle_down = wx.StaticText(self.panel, wx.ID_ANY, 'param.throttle_down')
        self.param_throttle_up = wx.StaticText(self.panel, wx.ID_ANY, 'param.throttle_up')
        self.param_throttle_deadband_on = wx.StaticText(self.panel, wx.ID_ANY, 'param.throttle_deadband_on')

        self.dominant_throttle_on = wx.StaticText(self.panel, wx.ID_ANY, 'dominant_throttle_on')
        self.rope_stuck_on = wx.StaticText(self.panel, wx.ID_ANY, 'rope_stuck_on')
        self.iq_alpha = wx.StaticText(self.panel, wx.ID_ANY, 'iq_alpha')
        self.speed_alpha = wx.StaticText(self.panel, wx.ID_ANY, 'speed_alpha')

    def define_textctrl(self):
        self.txtCtrl_cl_kp = wx.TextCtrl(self.panel, wx.ID_ANY,'0.23')
        self.txtCtrl_cl_ki = wx.TextCtrl(self.panel, wx.ID_ANY,'0.03')
        self.txtCtrl_sl_kp = wx.TextCtrl(self.panel, wx.ID_ANY,'15')
        self.txtCtrl_sl_ki = wx.TextCtrl(self.panel, wx.ID_ANY,'0.25')
        self.txtCtrl_sl_kt = wx.TextCtrl(self.panel, wx.ID_ANY,'1.0')

        self.txtCtrl_throttle_zero = wx.TextCtrl(self.panel, wx.ID_ANY,'0.499')
        self.txtCtrl_throttle_down = wx.TextCtrl(self.panel, wx.ID_ANY,'0.329')
        self.txtCtrl_throttle_up = wx.TextCtrl(self.panel, wx.ID_ANY,'0.674')
        self.txtCtrl_throttle_deadband_on = wx.TextCtrl(self.panel, wx.ID_ANY,'0.03')

        self.txtCtrl_dominant_throttle_on = wx.TextCtrl(self.panel, wx.ID_ANY,'1')
        self.txtCtrl_rope_stuck_on = wx.TextCtrl(self.panel, wx.ID_ANY,'1')
        self.txtCtrl_iq_alpha = wx.TextCtrl(self.panel, wx.ID_ANY,'0.005')
        self.txtCtrl_speed_alpha = wx.TextCtrl(self.panel, wx.ID_ANY,'0.05')

    def define_left_sizer(self):
        self.leftSizer1.Add(self.param_cl_kp, 0, wx.ALL, BORDER1)
        self.leftSizer1.Add(self.param_cl_ki, 0, wx.ALL, BORDER1)
        self.leftSizer1.Add(self.param_sl_kp, 0, wx.ALL, BORDER1)
        self.leftSizer1.Add(self.param_sl_ki, 0, wx.ALL, BORDER1)
        self.leftSizer1.Add(self.param_sl_kt, 0, wx.ALL, BORDER1)

        self.leftSizer2.Add(self.param_throttle_zero, 0, wx.ALL, BORDER1)
        self.leftSizer2.Add(self.param_throttle_down, 0, wx.ALL, BORDER1)
        self.leftSizer2.Add(self.param_throttle_up, 0, wx.ALL, BORDER1)
        self.leftSizer2.Add(self.param_throttle_deadband_on, 0, wx.ALL, BORDER1)

        self.leftSizer3.Add(self.dominant_throttle_on, 0, wx.ALL, BORDER1)
        self.leftSizer3.Add(self.rope_stuck_on, 0, wx.ALL, BORDER1)
        self.leftSizer3.Add(self.iq_alpha, 0, wx.ALL, BORDER1)
        self.leftSizer3.Add(self.speed_alpha, 0, wx.ALL, BORDER1)

    def define_right_sizer(self):
        self.rightSizer1.Add(self.txtCtrl_cl_kp, 1, wx.ALL, BORDER2)
        self.rightSizer1.Add(self.txtCtrl_cl_ki, 1, wx.ALL, BORDER2)
        self.rightSizer1.Add(self.txtCtrl_sl_kp, 1, wx.ALL, BORDER2)
        self.rightSizer1.Add(self.txtCtrl_sl_ki, 1, wx.ALL, BORDER2)
        self.rightSizer1.Add(self.txtCtrl_sl_kt, 1, wx.ALL, BORDER2)

        self.rightSizer2.Add(self.txtCtrl_throttle_zero, 1, wx.ALL, BORDER2)
        self.rightSizer2.Add(self.txtCtrl_throttle_down, 1, wx.ALL, BORDER2)
        self.rightSizer2.Add(self.txtCtrl_throttle_up, 1, wx.ALL, BORDER2)
        self.rightSizer2.Add(self.txtCtrl_throttle_deadband_on, 1, wx.ALL, BORDER2)

        self.rightSizer3.Add(self.txtCtrl_dominant_throttle_on, 1, wx.ALL, BORDER2)
        self.rightSizer3.Add(self.txtCtrl_rope_stuck_on, 1, wx.ALL, BORDER2)
        self.rightSizer3.Add(self.txtCtrl_iq_alpha, 1, wx.ALL, BORDER2)
        self.rightSizer3.Add(self.txtCtrl_speed_alpha, 1, wx.ALL, BORDER2)

    def onUpdate(self, event):

	if (self.connected == True):
	    # ----------------------------------------------------------------------------------------------------
            # current loop kp 
	    # ----------------------------------------------------------------------------------------------------
            newClKp = float(self.txtCtrl_cl_kp.GetValue())
	    if (newClKp == self.oldClKp):
		pass
	    else:
	        print 'Updated - cl.kp = %f' % newClKp
	    self.oldClKp = newClKp

	    # ----------------------------------------------------------------------------------------------------
            # current loop ki
	    # ----------------------------------------------------------------------------------------------------
            newClKi = float(self.txtCtrl_cl_ki.GetValue())
	    if (newClKi == self.oldClKi):
		pass
	    else:
	        print 'Updated - cl.ki = %f' % newClKi
	    self.oldClKi = newClKi

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
	    # Rope stuck on
	    # ----------------------------------------------------------------------------------------------------
            newRopeStuckOn = int(self.txtCtrl_rope_stuck_on.GetValue())
	    if (newRopeStuckOn == self.oldRope_stuck_on):
		pass
	    else:
                time.sleep(1)
	        # unicode mess ;-)
	        local_cmd = 'param set rope_stuck_on ' + self.txtCtrl_rope_stuck_on.GetValue().encode('ascii', 'ignore')
                serial_cmd(local_cmd, self.ser)
	        print 'Updated - rope_stuck_on = %d' % newRopeStuckOn
	    self.oldRope_stuck_on = newRopeStuckOn

	    # ----------------------------------------------------------------------------------------------------
	    # Iq alpha
	    # ----------------------------------------------------------------------------------------------------
            newIqAlpha = float(self.txtCtrl_iq_alpha.GetValue())
	    if (newIqAlpha == self.oldIqAlpha):
		pass
	    else:
                time.sleep(1)
	        # unicode mess ;-)
	        local_cmd = 'param set iq_alpha ' + self.txtCtrl_iq_alpha.GetValue().encode('ascii', 'ignore')
                serial_cmd(local_cmd, self.ser)
	        print 'Updated - iq_alpha = %f' % newIqAlpha
	    self.oldIqAlpha = newIqAlpha

	# if not connected then alert user
	else:
            self.lblConnected.SetForegroundColour(wx.Colour(255,0,0))
	    self.lblConnected.SetLabel('You must connect first!')

    def onConnect(self, event):
	try:
	    self.connected = True
            self.ser = serial.Serial(port = '/dev/tty'+self.combo.GetValue(),
                                     baudrate = 9600,
                                     parity = serial.PARITY_NONE,
                                     stopbits = serial.STOPBITS_ONE,
                                     bytesize = serial.EIGHTBITS,
                                     timeout = 1)

            self.lblConnected.SetForegroundColour(wx.Colour(11, 102 , 66))
	    self.lblConnected.SetLabel("Connected to " + self.combo.GetValue())

	except:
            self.lblConnected.SetForegroundColour(wx.Colour(255,0,0))
	    self.lblConnected.SetLabel('Cannot connect')

    def onTestInject(self, event):

	if (self.toggle == False):
	    try:
                serial_cmd('param set ti 1', self.ser)
	    except:
	        print 'No connection'

	    self.testInjectBtn.SetBackgroundColour(GREEN)
	    self.toggle = True
	else:
	    try:
                serial_cmd('param set ti 0', self.ser)
	    except:
	        print 'No connection'
	    self.testInjectBtn.SetBackgroundColour(INJECT_COLOR)
	    self.toggle = False

    def onGetIq(self, event):
	serial_cmd('get_iq', self.ser)


    def onQuit(self, event):
        self.Close()

    def onCombo(self, event):
        print 'Selected port: ' + self.combo.GetValue()
	#self.label.SetLabel("selected "+ self.combo.GetValue() +" from Combobox") 
        #print('Connected to: ' + self.ser.portstr)


if __name__ == '__main__':
    app = wx.App()
    frame = MyForm().Show()
    app.MainLoop()
