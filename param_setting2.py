#!/usr/bin/python

# Author      : Heinz Samuelsson
# Date        : ons 10 maj 2017 10:00:55 CEST
# File        : param_setting2.py
# Reference   : -
# Description : Application is used to set parameters for ActSafe's Ascender ACX and TCX.
#               Icons:
#                  http://www.iconarchive.com/show/soft-scraps-icons-by-hopstarter/Button-Play-icon.html
#                  http://www.iconarchive.com/show/colorful-long-shadow-icons-by-graphicloads/Button-eject-icon.html

#    param list
#    motor.cl.kp: 0.229996
#    motor.cl.ki: 0.030518
#    motor.cl.kt: 1.000000
#    motor.cl.max: 51.000000
#    motor.cl.min: -51.000000
#    motor.sl.kp: 15.000000
#    motor.sl.ki: 0.250000
#    motor.sl.kt: 0.125000
#    motor.sl.max: 80.000000
#    motor.sl.min: -80.000000
#    trajec.acc: 80.000000
#    trajec.ret: 320.000000
#    throttle.zero: 0.501099
#    throttle.down: 0.328705
#    throttle.up: 0.672745
#    throttle.deadband_on: 0.030518
#    throttle.deadband_off: 0.027466
#    throttle.has_switch: 1
#    num_motor_ch: 1
#    power_out: 300.000000
#    power_in: 100.000000
#    brake_temp_ok: 60.000000
#    brake_temp_hi: 65.000000
#    brake_max_id: 40.000000
#    angle_offset: 0.473084
#    alignment_current: 40.000000
#    sin_bias: 0.050049
#    sin_gain: 4.946854
#    cos_bias: 0.051147
#    cos_gain: 4.949844
#    brake_test.pos_ratio: 0.399994
#    brake_test.neg_ratio: 0.199997
#    psu_ok: 0
#    led.brightness_hi: 0.300003
#    led.brightness_lo: 0.300003
#    idreg.kp: 0.009995
#    idreg.ki: 0.001007
#    idreg.kt: 0.500000
#    power_margin: 0.000000
#    power_factor: 1.000000
#    speed_filter: 2147483
#    max_motor_temp: 100.000000
#    idle_timeout: 14400
#    remote_ctrl_timeout: 10
#    soc_lim_run_up: 8
#    max_drive_temp: 85.000000
#    dominant_throttle_on: 1
#    rope_stuck_on: 1
#    iq_alpha: 0.005005
#    speed_alpha: 0.050003
#    mx: 40.000000
#    mi: -39.999984
#    delay_start: 5000
#    speed_lim: 5.000000
#    undershoot: -0.999985
#    ti: 0


import wx
import time
import serial  
import base64
import sys

WINDOW_SIZE = (1035, 730)

# sizer borders
BORDER1 = 5
STATIC_BOX_SERIAL_BORDER = 10
STATIC_BOX_PARAMS_BORDER = 5
PARAMSIZER1_BORDER = 2
PARAMSIZER2_BORDER = 2
PARAMSIZER3_BORDER = 5
PARAMSIZER4_BORDER = 2

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

def serial_read(cmd, no, serial):
    # send command to serial port
    serial.write(cmd+'\r');
    serial.reset_input_buffer()
    serial.reset_output_buffer()
    serial.flush()

    # read data from serial port
    c = serial.read(no)
    return c


class MyForm(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title='Built in Configuration Tool, Ascender ACX/TCX', style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER, size=WINDOW_SIZE)
        self.panel = wx.Panel(self, wx.ID_ANY, style=wx.BORDER_RAISED)

	try:
            licFile = open("licensfile.lic", "r")
            licDate = licFile.readline()
	    decodecDate = base64.b64decode(licDate.decode())

	    strippedDate = decodecDate.strip('\n')
            splitDate = strippedDate.split('-')
            trigger = 0

            if (int(splitDate[0]) <= 2017):
                if (int(splitDate[1]) < 5):
                    trigger = 1
                else:    
                    if (int(splitDate[2]) < 22):
                        trigger = 1

            if (trigger == 0):
                print 'License OK'
            else:
                print 'License has expiered:', strippedDate
                sys.exit()

        except:
            print 'No license file'
            sys.exit()

	# flag if function is active
	self.toggle      = False
	self.connected   = False
	self.runningUp   = False
	self.runningDown = False

	# flag to check if parameters have been updated
	self.oldSlKi = 0.25
	self.oldDominantThrottle = 1
	self.oldIqAlpha = 0.005
	self.oldSpeedAlpha = 0.05
	self.oldUndershoot = -1.0
	self.oldRopeStuckOn = 1
	self.oldDelaySpeed = 5000

	self.exitDialog =  wx.MessageDialog( self, " Quit application? \nCheck that motor has stopped!\n", "Quit", wx.YES_NO)

	#self.Centre()
	self.SetPosition((2500, 100))

	self.load_bitmaps()          # images for up/down/stop buttons 
	self.defineCombo()           # combo box for port names
	self.define_buttons()
	self.define_spin_control()   # spin control for motor speed
        self.txtSerialPort = wx.StaticText(self.panel, wx.ID_ANY, 'Select serial port')

	# Ascender parameters
	self.define_parameters()
	self.define_textctrl_parameters()
	self.disable_txt_controls()

        headline = '       - ACX/TXC logging - \n'
	self.txtMultiCtrl = wx.TextCtrl(self.panel, -1, headline, size=(180, 690), style=wx.TE_MULTILINE)
        self.txtMultiCtrl.SetInsertionPoint(0)

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
	self.rightSizer.Add(self.btnQuit, 0, wx.LEFT, 160)
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
	self.buttonSizer2 = wx.BoxSizer(wx.HORIZONTAL)
	self.buttonSizer2.Add(self.param_delay_start, 1, wx.ALL, 5)
	self.buttonSizer2.Add(self.txtCtrl_delay_start, 1, wx.ALL, 5)
        self.staticBoxSizer3 = wx.StaticBoxSizer(self.statBoxEnhMeas, wx.VERTICAL)
	self.staticBoxSizer3.Add(self.paramSizer3, 1, wx.ALL, 5)
	self.staticBoxSizer3.Add(self.buttonSizer2, 1, wx.ALL, 5)
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

        self.topSizer = wx.BoxSizer(wx.HORIZONTAL)
	self.leftTopSizer = wx.BoxSizer(wx.VERTICAL)
        self.leftTopSizer.Add(self.staticBoxSizer1, 0, wx.ALL|wx.EXPAND, BORDER1)
        self.leftTopSizer.Add(self.staticBoxSizer2, 1, wx.ALL|wx.EXPAND, BORDER1)
        self.leftTopSizer.Add(self.staticBoxSizer3, 1, wx.ALL|wx.EXPAND, BORDER1)
        self.leftTopSizer.Add(self.staticBoxSizer4, 1, wx.ALL|wx.EXPAND, BORDER1)
	self.topSizer.Add(self.leftTopSizer, 0, wx.ALL, BORDER1)
	self.topSizer.Add(self.txtMultiCtrl, 0, wx.TOP, 20)

        self.panel.SetSizer(self.topSizer)

    def load_bitmaps(self):
	self.bmpUp = wx.Bitmap("up.png", wx.BITMAP_TYPE_ANY)
	self.bmpDown = wx.Bitmap("up2.png", wx.BITMAP_TYPE_ANY)
	self.bmpStop = wx.Bitmap("stop.png", wx.BITMAP_TYPE_ANY)
    
    def define_buttons(self):
        self.btnConnected = wx.Button(self.panel, wx.ID_ANY, 'Connect')
	self.lblConnected = wx.StaticText(self.panel, label= 'Not connected                                 ')
        self.btnConfig = wx.Button(self.panel, wx.ID_ANY, 'Configure     ')
        self.btnTestInject = wx.Button(self.panel, wx.ID_ANY, 'Test Inject')
	self.btnTestInject.SetBackgroundColour(BROWN)
        self.btnGetIq = wx.Button(self.panel, wx.ID_ANY, 'get_iq')
        self.btnQuit = wx.Button(self.panel, wx.ID_ANY, 'Quit')
        self.btnTestRunUp = wx.BitmapButton(self.panel, wx.ID_ANY, bitmap=self.bmpUp)
        self.btnTestRunDown = wx.BitmapButton(self.panel, wx.ID_ANY, bitmap=self.bmpDown)
        self.btnTestStop = wx.BitmapButton(self.panel, wx.ID_ANY, bitmap=self.bmpStop)
        self.btnConfig2 = wx.Button(self.panel, wx.ID_ANY, 'Configure     ')

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
        self.param_par4 = wx.StaticText(self.panel, wx.ID_ANY, 'par4')
        self.param_delay_start = wx.StaticText(self.panel, wx.ID_ANY, 'delay_start')

    def define_textctrl_parameters(self):
        self.txtCtrl_cl_kp = wx.TextCtrl(self.panel, wx.ID_ANY,'0.23')
        self.txtCtrl_cl_ki = wx.TextCtrl(self.panel, wx.ID_ANY,'13')
        self.txtCtrl_sl_kp = wx.TextCtrl(self.panel, wx.ID_ANY,'15')
        self.txtCtrl_sl_ki = wx.TextCtrl(self.panel, wx.ID_ANY,'0.25')
        self.txtCtrl_throttle_zero = wx.TextCtrl(self.panel, wx.ID_ANY,'25')
        self.txtCtrl_throttle_down = wx.TextCtrl(self.panel, wx.ID_ANY,'0.5')
        self.txtCtrl_throttle_up = wx.TextCtrl(self.panel, wx.ID_ANY,'4')
        self.txtCtrl_throttle_deadband_on = wx.TextCtrl(self.panel, wx.ID_ANY,'0.95')
        self.txtCtrl_dominant_throttle_on = wx.TextCtrl(self.panel, wx.ID_ANY,'1')
        self.txtCtrl_rope_stuck_on = wx.TextCtrl(self.panel, wx.ID_ANY,'1')
        self.txtCtrl_iq_alpha = wx.TextCtrl(self.panel, wx.ID_ANY,'0.005')
        self.txtCtrl_speed_alpha = wx.TextCtrl(self.panel, wx.ID_ANY,'0.05')
        self.txtCtrl_undershoot = wx.TextCtrl(self.panel, wx.ID_ANY,'-1.0')
        self.txtCtrl_par4 = wx.TextCtrl(self.panel, wx.ID_ANY,'0.3')
        self.txtCtrl_delay_start = wx.TextCtrl(self.panel, wx.ID_ANY,'5000')

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
	self.paramSizer2.Add(self.param_throttle_zero, 0, wx.ALL, PARAMSIZER2_BORDER)
	self.paramSizer2.Add(self.txtCtrl_throttle_zero, 0, wx.ALL, PARAMSIZER2_BORDER)
	self.paramSizer2.Add(self.param_throttle_down, 0, wx.ALL, PARAMSIZER2_BORDER)
	self.paramSizer2.Add(self.txtCtrl_throttle_down, 0, wx.ALL, PARAMSIZER2_BORDER)
	self.paramSizer2.Add(self.param_throttle_up, 0, wx.ALL, PARAMSIZER2_BORDER)
	self.paramSizer2.Add(self.txtCtrl_throttle_up, 0, wx.ALL, PARAMSIZER2_BORDER)

    def create_sizer3(self):
	self.paramSizer3 = wx.BoxSizer(wx.HORIZONTAL)
	self.paramSizer3.Add(self.param_rope_stuck_on, 0, wx.ALL, PARAMSIZER3_BORDER)
	self.paramSizer3.Add(self.txtCtrl_rope_stuck_on, 0, wx.ALL, PARAMSIZER3_BORDER)
	self.paramSizer3.Add(self.param_iq_alpha, 0, wx.ALL, PARAMSIZER3_BORDER)
	self.paramSizer3.Add(self.txtCtrl_iq_alpha, 0, wx.ALL, PARAMSIZER3_BORDER)
	self.paramSizer3.Add(self.param_speed_alpha, 0, wx.ALL, PARAMSIZER3_BORDER)
	self.paramSizer3.Add(self.txtCtrl_speed_alpha, 0, wx.ALL, PARAMSIZER3_BORDER)
	self.paramSizer3.Add(self.param_undershoot, 0, wx.ALL, PARAMSIZER3_BORDER)
	self.paramSizer3.Add(self.txtCtrl_undershoot, 0, wx.ALL, PARAMSIZER3_BORDER)

    def create_sizer4(self):
	self.paramSizer4 = wx.BoxSizer(wx.VERTICAL)
	self.paramSizer4.Add(self.param_throttle_deadband_on, 0, wx.ALL, PARAMSIZER4_BORDER)
	self.paramSizer4.Add(self.txtCtrl_throttle_deadband_on, 0, wx.ALL, PARAMSIZER4_BORDER)
	self.paramSizer4.Add(self.param_dominant_throttle_on, 0, wx.ALL, PARAMSIZER4_BORDER)
	self.paramSizer4.Add(self.txtCtrl_dominant_throttle_on, 0, wx.ALL, PARAMSIZER4_BORDER)
	self.paramSizer4.Add(self.param_par4, 0, wx.ALL, PARAMSIZER4_BORDER)
	self.paramSizer4.Add(self.txtCtrl_par4, 0, wx.ALL, PARAMSIZER4_BORDER)

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
	    self.txtMultiCtrl.AppendText('Connected' + "\n")


        except:
            self.lblConnected.SetForegroundColour(wx.Colour(255,0,0))
            self.lblConnected.SetLabel('Cannot connect')

        self.read_param_list()
    
    def read_param_list(self):

	if (self.connected == True):
            time.sleep(1)
	    rv = serial_read('param list', 1320, self.ser)
	    newrv = rv.split("\n")
	    print newrv

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
	        self.txtMultiCtrl.AppendText('sl.ki updated' + "\n")

	    self.oldSlKi = newSlKi

	    # ----------------------------------------------------------------------------------------------------
	    # Dominant throttle
	    # ----------------------------------------------------------------------------------------------------
            newDominantThrottle = int(self.txtCtrl_dominant_throttle_on.GetValue())
	    if (newDominantThrottle > 1 or newDominantThrottle < 0):
	        self.txtCtrl_dominant_throttle_on.SetForegroundColour((RED))

	    else:
	        if (newDominantThrottle == self.oldDominantThrottle):
	            self.txtCtrl_dominant_throttle_on.SetForegroundColour((BLACK))
	        else:
	            self.txtCtrl_dominant_throttle_on.SetForegroundColour((BLACK))
                    time.sleep(1)
	            # unicode mess ;-)
	            local_cmd = 'param set dominant_throttle_on ' + self.txtCtrl_dominant_throttle_on.GetValue().encode('ascii', 'ignore')
                    serial_cmd(local_cmd, self.ser)
	            self.txtMultiCtrl.AppendText('dominant_throttle_on updated' + "\n")

	        self.oldDominantThrottle = newDominantThrottle

	    # ----------------------------------------------------------------------------------------------------
	    # iq alpha
	    # ----------------------------------------------------------------------------------------------------
            newIqAlpha = float(self.txtCtrl_iq_alpha.GetValue())
	    if (newIqAlpha == self.oldIqAlpha):
		pass
	    else:
                time.sleep(1)
	        # unicode mess ;-)
	        local_cmd = 'param set iq_alpha ' + self.txtCtrl_iq_alpha.GetValue().encode('ascii', 'ignore')
                serial_cmd(local_cmd, self.ser)
	        self.txtMultiCtrl.AppendText('iq_alpha updated' + "\n")

	    self.oldIqAlpha = newIqAlpha

	    # ----------------------------------------------------------------------------------------------------
	    # speed alpha
	    # ----------------------------------------------------------------------------------------------------
            newSpeedAlpha = float(self.txtCtrl_speed_alpha.GetValue())
	    if (newSpeedAlpha == self.oldSpeedAlpha):
		pass
	    else:
                time.sleep(1)
	        # unicode mess ;-)
	        local_cmd = 'param set speed_alpha ' + self.txtCtrl_speed_alpha.GetValue().encode('ascii', 'ignore')
                serial_cmd(local_cmd, self.ser)
	        self.txtMultiCtrl.AppendText('speed_alpha updated' + "\n")

	    self.oldSpeedAlpha = newSpeedAlpha

	    # ----------------------------------------------------------------------------------------------------
	    # undershoot
	    # ----------------------------------------------------------------------------------------------------
            newUndershoot = float(self.txtCtrl_undershoot.GetValue())
	    if (newUndershoot == self.oldUndershoot):
		pass
	    else:
                time.sleep(1)
	        # unicode mess ;-)
	        local_cmd = 'param set undershoot ' + self.txtCtrl_undershoot.GetValue().encode('ascii', 'ignore')
                serial_cmd(local_cmd, self.ser)
	        self.txtMultiCtrl.AppendText('undershoot updated' + "\n")

	    self.oldUndershoot = newUndershoot

	    # ----------------------------------------------------------------------------------------------------
	    # rope_stuck_no
	    # ----------------------------------------------------------------------------------------------------
            newRopeStuckOn = int(self.txtCtrl_rope_stuck_on.GetValue())
	    if (newRopeStuckOn > 1 or newRopeStuckOn < 0):
                self.txtCtrl_rope_stuck_on.SetForegroundColour((RED))

            else:
	        if (newRopeStuckOn == self.oldRopeStuckOn):
                    self.txtCtrl_rope_stuck_on.SetForegroundColour((BLACK))
	        else:
                    self.txtCtrl_rope_stuck_on.SetForegroundColour((BLACK))
                    time.sleep(1)
	            # unicode mess ;-)
	            local_cmd = 'param set rope_stuck_on ' + self.txtCtrl_rope_stuck_on.GetValue().encode('ascii', 'ignore')
                    serial_cmd(local_cmd, self.ser)
	            self.txtMultiCtrl.AppendText('rope_stuck_on updated' + "\n")

	        self.oldRopeStuckOn = newRopeStuckOn

	else:
            self.lblConnected.SetForegroundColour(wx.Colour(255,0,0))
	    self.lblConnected.SetLabel('You must connect first!')

    def onTestRunUp(self, event):

        if (self.connected == True):
            self.btnTestRunDown.Enable(False)
            speedValue = self.scSpeed.GetValue()

	    if (self.runningUp == False):
	        self.txtMultiCtrl.AppendText('Up command ' + "\n")
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
	        self.txtMultiCtrl.AppendText('Down command ' + "\n")
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
	self.txtMultiCtrl.AppendText('Stop command ' + "\n")
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
	        self.txtMultiCtrl.AppendText('Inject On' + "\n")
                serial_cmd('param set ti 1', self.ser)
	        self.btnTestInject.SetBackgroundColour(RED)
	        self.toggle = True
	    except:
                self.lblConnected.SetForegroundColour(wx.Colour(255,0,0))
	        self.lblConnected.SetLabel('You must connect first!')

	else:
	    try:
	        self.txtMultiCtrl.AppendText('Inject Off' + "\n")
                serial_cmd('param set ti 0', self.ser)
	        self.btnTestInject.SetBackgroundColour(BROWN)
	        self.toggle = False
	    except:
                self.lblConnected.SetForegroundColour(wx.Colour(255,0,0))
	        self.lblConnected.SetLabel('You must connect first!')

    def onGetIq(self, event):
	try:
	    self.txtMultiCtrl.AppendText('get_iq ' + "\n")
	    rv = serial_read('get_iq', 64, self.ser)
	    self.txtMultiCtrl.AppendText(rv[6:21])
	    self.txtMultiCtrl.AppendText(rv[22:36])
	    self.txtMultiCtrl.AppendText(rv[37:59] + "\n")
	except:
            self.lblConnected.SetForegroundColour(wx.Colour(255,0,0))
	    self.lblConnected.SetLabel('You must connect first!')

    def onCombo(self, event):
        print 'Selected port: ' + self.combo.GetValue()

    def onQuit(self, event):
        rv = self.exitDialog.ShowModal()

        if rv == wx.ID_YES:
            self.Close(True)


if __name__ == '__main__':
    app = wx.App()
    frame = MyForm().Show()
    app.MainLoop()
