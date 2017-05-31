import wx
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub as Publisher

BORDER1 = 5
TEXT_SERIAL_PORT_BORDER = 10

GREY  = (180, 180, 180)
BLACK = (0, 0, 0)


def serial_cmd(cmd, serial):
    # send command to serial port
    try:
        serial.write(cmd + '\r');
    except:
        print 'Not Connected!'

class ProdTestForm(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

	# Add a panel so it looks the correct on all platforms
        #self.panel = wx.Panel(self, wx.ID_ANY)

	serialSizer = self.setup_serial_sizer()
	configParamsSizer = self.setup_config_params()
	enhancedMeasSizer = self.setup_test_enahanced_measuring()
	testRun = self.setup_test_run()
        multiTextControl = self.setup_multi_text_control()

	leftTopSizer = wx.BoxSizer(wx.VERTICAL)
        leftTopSizer.Add(serialSizer, 0, wx.ALL|wx.EXPAND, BORDER1)
        leftTopSizer.Add(configParamsSizer, 0, wx.ALL|wx.EXPAND, BORDER1)
        leftTopSizer.Add(enhancedMeasSizer, 0, wx.ALL|wx.EXPAND, BORDER1)
        leftTopSizer.Add(testRun, 0, wx.ALL|wx.EXPAND, BORDER1)
        leftTopSizer.Add(multiTextControl, 0, wx.ALL|wx.EXPAND, BORDER1)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
	topSizer.Add(leftTopSizer, 0, wx.ALL, BORDER1)

        self.SetSizer(topSizer)
	self.lock_text_controls()
	Publisher.subscribe(self.readmsg, ("show.mainframe"))

    def readmsg(self, msg):
        self.pubsubText.SetValue(msg.data)

    def setup_serial_sizer(self):
        txtSerialPort = wx.StaticText(self, wx.ID_ANY, 'Select serial port')
	txtSerPortSizer = wx.BoxSizer(wx.HORIZONTAL)
	txtSerPortSizer.Add(txtSerialPort, 0, wx.TOP, TEXT_SERIAL_PORT_BORDER)

        portNames = ['ACM0', 'ACM1', 'USB0']
        comboBox = wx.ComboBox(self, choices=portNames)
        comboBox.SetSelection(0) # preselect ACM0
        comboBox.Bind(wx.EVT_COMBOBOX, self.onCombo)
	comboSizer = wx.BoxSizer(wx.HORIZONTAL)
	comboSizer.Add(comboBox, 0, wx.TOP, 10)

	statBoxSerial = wx.StaticBox(self, wx.ID_ANY, '  Serial connection    ')
	statBoxSerial.SetBackgroundColour(GREY)
	statBoxSerial.SetForegroundColour(BLACK)
        statBoxSizer = wx.StaticBoxSizer(statBoxSerial, wx.HORIZONTAL)

        btnConnect = wx.Button(self, wx.ID_ANY, 'Connect')
        self.Bind(wx.EVT_BUTTON, self.onConnect, btnConnect)
	lblConnect = wx.StaticText(self, label= 'Not connected')

        btnQuit = wx.Button(self, wx.ID_ANY, 'Quit')
	btnQuitSizer = wx.BoxSizer(wx.HORIZONTAL)
	btnQuitSizer.Add(btnQuit, 0, wx.ALL, 20)

        statBoxSizer.Add(txtSerPortSizer, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 15)
        statBoxSizer.Add(comboSizer, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 10)
        statBoxSizer.Add(btnConnect, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 20)
        statBoxSizer.Add(lblConnect, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 25)
        statBoxSizer.Add(btnQuitSizer, 0, wx.LEFT, 420)

	return statBoxSizer

    def setup_config_params(self):

        param_cl_max = wx.StaticText(self, wx.ID_ANY, 'cl.max')
        self.txtCtrl_cl_max = wx.TextCtrl(self, wx.ID_ANY,'51.00')
        param_cl_min = wx.StaticText(self, wx.ID_ANY, 'cl.min')
        self.txtCtrl_cl_min = wx.TextCtrl(self, wx.ID_ANY,'-51.00')
        param_sl_ki = wx.StaticText(self, wx.ID_ANY, 'sl.ki')
        self.txtCtrl_sl_ki = wx.TextCtrl(self, wx.ID_ANY,'0.25000')

        param_sl_max = wx.StaticText(self, wx.ID_ANY, 'sl.max')
        self.txtCtrl_sl_max = wx.TextCtrl(self, wx.ID_ANY,'80.00')
        param_sl_min = wx.StaticText(self, wx.ID_ANY, 'sl.min')
        self.txtCtrl_sl_min = wx.TextCtrl(self, wx.ID_ANY,'-80.00')
        param_has_switch = wx.StaticText(self, wx.ID_ANY, 'has_switch')
        self.txtCtrl_has_switch = wx.TextCtrl(self, wx.ID_ANY,'1')

        param_power_margin = wx.StaticText(self, wx.ID_ANY, 'power_margin')
        self.txtCtrl_power_margin = wx.TextCtrl(self, wx.ID_ANY,'0.0000')
        param_power_factor = wx.StaticText(self, wx.ID_ANY, 'power_factor')
        self.txtCtrl_power_factor = wx.TextCtrl(self, wx.ID_ANY,'1.0000')
        param_brightness_lo = wx.StaticText(self, wx.ID_ANY, 'brightness_lo')
        self.txtCtrl_brightness_lo = wx.TextCtrl(self, wx.ID_ANY,'1.0000')

        param_brake_temp_ok = wx.StaticText(self, wx.ID_ANY, 'brake_temp_ok')
        self.txtCtrl_brake_temp_ok = wx.TextCtrl(self, wx.ID_ANY,'60.0000')
        param_brake_temp_hi = wx.StaticText(self, wx.ID_ANY, 'brake_temp_hi')
        self.txtCtrl_brake_temp_hi = wx.TextCtrl(self, wx.ID_ANY,'65.0000')
        param_brake_max_id = wx.StaticText(self, wx.ID_ANY, 'brake_max_id')
        self.txtCtrl_brake_max_id = wx.TextCtrl(self, wx.ID_ANY,'40.0000')

        param_brake_pos_ratio = wx.StaticText(self, wx.ID_ANY, 'brake_pos_ratio')
        self.txtCtrl_brake_pos_ratio = wx.TextCtrl(self, wx.ID_ANY,'0.39999')
        param_trajec_acc = wx.StaticText(self, wx.ID_ANY, 'trajec.acc')
        self.txtCtrl_trajec_acc = wx.TextCtrl(self, wx.ID_ANY,'80.0000')
        param_trajec_ret = wx.StaticText(self, wx.ID_ANY, 'trajec.ret')
        self.txtCtrl_trajec_ret = wx.TextCtrl(self, wx.ID_ANY,'320.000')

        param_dominant_throttle_on = wx.StaticText(self, wx.ID_ANY, 'dominant_throttle_on')
        self.txtCtrl_dominant_throttle_on = wx.TextCtrl(self, wx.ID_ANY,'1')
        param_max_motor_temp = wx.StaticText(self, wx.ID_ANY, 'max_motor_temp')
        self.txtCtrl_max_motor_temp = wx.TextCtrl(self, wx.ID_ANY,'100.000')
        param_num_motor_ch = wx.StaticText(self, wx.ID_ANY, 'num_motor_ch')
        self.txtCtrl_num_motor_ch = wx.TextCtrl(self, wx.ID_ANY,'1')

        param_idle_timeout = wx.StaticText(self, wx.ID_ANY, 'idle_timeout')
        self.txtCtrl_idle_timeout = wx.TextCtrl(self, wx.ID_ANY,'14400')

        btnConfigure = wx.Button(self, wx.ID_ANY, ' Configure   ')
        self.Bind(wx.EVT_BUTTON, self.onConfigure, btnConfigure)
        btnSaveParam = wx.Button(self, wx.ID_ANY, ' Save Param')
        self.Bind(wx.EVT_BUTTON, self.onSaveParam, btnSaveParam)
	btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(btnConfigure, 0, wx.LEFT, 10)
        btnSizer.Add(btnSaveParam, 0, wx.LEFT, 10)

	paramSizer1 = wx.BoxSizer(wx.VERTICAL)
	paramSizer1.Add(param_cl_max, 0, wx.TOP, 10)
	paramSizer1.Add(self.txtCtrl_cl_max, 0, wx.TOP, 10)
	paramSizer1.Add(param_cl_min, 0, wx.TOP, 10)
	paramSizer1.Add(self.txtCtrl_cl_min, 0, wx.TOP, 10)
	paramSizer1.Add(param_sl_ki, 0, wx.TOP, 10)
	paramSizer1.Add(self.txtCtrl_sl_ki, 0, wx.TOP, 10)

	paramSizer2 = wx.BoxSizer(wx.VERTICAL)
	paramSizer2.Add(param_sl_max, 0, wx.TOP, 10)
	paramSizer2.Add(self.txtCtrl_sl_max, 0, wx.TOP, 10)
	paramSizer2.Add(param_sl_min, 0, wx.TOP, 10)
	paramSizer2.Add(self.txtCtrl_sl_min, 0, wx.TOP, 10)
	paramSizer2.Add(param_has_switch, 0, wx.TOP, 10)
	paramSizer2.Add(self.txtCtrl_has_switch, 0, wx.TOP, 10)

	paramSizer3 = wx.BoxSizer(wx.VERTICAL)
	paramSizer3.Add(param_power_margin, 0, wx.TOP, 10)
	paramSizer3.Add(self.txtCtrl_power_margin, 0, wx.TOP, 10)
	paramSizer3.Add(param_power_factor, 0, wx.TOP, 10)
	paramSizer3.Add(self.txtCtrl_power_factor, 0, wx.TOP, 10)
	paramSizer3.Add(param_brightness_lo, 0, wx.TOP, 10)
	paramSizer3.Add(self.txtCtrl_brightness_lo, 0, wx.TOP, 10)

	paramSizer4 = wx.BoxSizer(wx.VERTICAL)
	paramSizer4.Add(param_brake_temp_ok, 0, wx.TOP, 10)
	paramSizer4.Add(self.txtCtrl_brake_temp_ok, 0, wx.TOP, 10)
	paramSizer4.Add(param_brake_temp_hi, 0, wx.TOP, 10)
	paramSizer4.Add(self.txtCtrl_brake_temp_hi, 0, wx.TOP, 10)
	paramSizer4.Add(param_brake_max_id, 0, wx.TOP, 10)
	paramSizer4.Add(self.txtCtrl_brake_max_id, 0, wx.TOP, 10)

	paramSizer5 = wx.BoxSizer(wx.VERTICAL)
	paramSizer5.Add(param_brake_pos_ratio, 0, wx.TOP, 10)
	paramSizer5.Add(self.txtCtrl_brake_pos_ratio, 0, wx.TOP, 10)
	paramSizer5.Add(param_trajec_acc, 0, wx.TOP, 10)
	paramSizer5.Add(self.txtCtrl_trajec_acc, 0, wx.TOP, 10)
	paramSizer5.Add(param_trajec_ret, 0, wx.TOP, 10)
	paramSizer5.Add(self.txtCtrl_trajec_ret, 0, wx.TOP, 10)

	paramSizer6 = wx.BoxSizer(wx.VERTICAL)
	paramSizer6.Add(param_dominant_throttle_on, 0, wx.TOP, 10)
	paramSizer6.Add(self.txtCtrl_dominant_throttle_on, 0, wx.TOP, 10)
	paramSizer6.Add(param_max_motor_temp, 0, wx.TOP, 10)
	paramSizer6.Add(self.txtCtrl_max_motor_temp, 0, wx.TOP, 10)
	paramSizer6.Add(param_num_motor_ch, 0, wx.TOP, 10)
	paramSizer6.Add(self.txtCtrl_num_motor_ch, 0, wx.TOP, 10)

	paramSizer7 = wx.BoxSizer(wx.VERTICAL)
	paramSizer7.Add(param_idle_timeout, 0, wx.TOP, 10)
	paramSizer7.Add(self.txtCtrl_idle_timeout, 0, wx.TOP, 10)

	paramTopSizer = wx.BoxSizer(wx.HORIZONTAL)
	paramTopSizer.Add(paramSizer1, 0, wx.ALL, 10)
	paramTopSizer.Add(paramSizer2, 0, wx.ALL, 10)
	paramTopSizer.Add(paramSizer3, 0, wx.ALL, 10)
	paramTopSizer.Add(paramSizer4, 0, wx.ALL, 10)
	paramTopSizer.Add(paramSizer5, 0, wx.ALL, 10)
	paramTopSizer.Add(paramSizer6, 0, wx.ALL, 10)
	paramTopSizer.Add(paramSizer7, 0, wx.ALL, 10)

	statBoxConfigParams = wx.StaticBox(self, wx.ID_ANY, '  Set paramters')
	statBoxConfigParams.SetBackgroundColour(GREY)
	statBoxConfigParams.SetForegroundColour(BLACK)
        statBoxSizer = wx.StaticBoxSizer(statBoxConfigParams, wx.VERTICAL)

        statBoxSizer.Add(paramTopSizer, 0, wx.ALL, 10)
	statBoxSizer.Add(btnSizer, 0, wx.ALL, 10)

	return statBoxSizer

    def setup_test_enahanced_measuring(self):

        param_rope_stuck_on = wx.StaticText(self, wx.ID_ANY, 'rope_stuck_on')
        self.txtCtrl_rope_stuck_on = wx.TextCtrl(self, wx.ID_ANY,'1')
        param_iq_alpha = wx.StaticText(self, wx.ID_ANY, 'iq_alpha')
        self.txtCtrl_iq_alpha = wx.TextCtrl(self, wx.ID_ANY,'0.005')
        param_speed_alpha = wx.StaticText(self, wx.ID_ANY, 'speed_alpha')
        self.txtCtrl_speed_alpha = wx.TextCtrl(self, wx.ID_ANY,'0.05')
        param_undershoot = wx.StaticText(self, wx.ID_ANY, 'undershoot')
        self.txtCtrl_undershoot = wx.TextCtrl(self, wx.ID_ANY,'-1.0')
        param_delay_start = wx.StaticText(self, wx.ID_ANY, 'delay_start')
        self.txtCtrl_delay_start = wx.TextCtrl(self, wx.ID_ANY,'5000')

        btnConfigure = wx.Button(self, wx.ID_ANY, ' Configure   ')
        self.Bind(wx.EVT_BUTTON, self.onConfigure, btnConfigure)
        btnTestInject = wx.Button(self, wx.ID_ANY, ' Test Inject ')
        self.Bind(wx.EVT_BUTTON, self.onTestInject, btnTestInject)
        btnGetIq = wx.Button(self, wx.ID_ANY, '    Get iq          ')
        self.Bind(wx.EVT_BUTTON, self.onGetIq, btnGetIq)
        btnSaveParam = wx.Button(self, wx.ID_ANY, ' Save Param')
        self.Bind(wx.EVT_BUTTON, self.onSaveParam, btnSaveParam)

	paramSizer1 = wx.BoxSizer(wx.HORIZONTAL)
	paramSizer1.Add(param_rope_stuck_on, 0, wx.LEFT, 10)
	paramSizer1.Add(param_iq_alpha, 0, wx.LEFT, 14)
	paramSizer1.Add(param_speed_alpha, 0, wx.LEFT, 44)
	paramSizer1.Add(param_undershoot, 0, wx.LEFT, 24)
	paramSizer1.Add(param_delay_start, 0, wx.LEFT, 24)

	paramSizer2 = wx.BoxSizer(wx.HORIZONTAL)
	paramSizer2.Add(self.txtCtrl_rope_stuck_on, 0, wx.RIGHT, 10)
	paramSizer2.Add(self.txtCtrl_iq_alpha, 0, wx.LEFT, 15)
	paramSizer2.Add(self.txtCtrl_speed_alpha, 0, wx.LEFT, 15)
	paramSizer2.Add(self.txtCtrl_undershoot, 0, wx.LEFT, 15)
	paramSizer2.Add(self.txtCtrl_delay_start, 0, wx.LEFT, 15)

	paramSizer3 = wx.BoxSizer(wx.HORIZONTAL)
	paramSizer3.Add(btnConfigure, 0, wx.RIGHT, 10)
	paramSizer3.Add(btnTestInject, 0, wx.LEFT, 15)
	paramSizer3.Add(btnGetIq, 0, wx.LEFT, 15)
	paramSizer3.Add(btnSaveParam, 0, wx.LEFT, 15)

	statBoxTestEnhanced = wx.StaticBox(self, wx.ID_ANY, '  Test Enhanced Measuring')
	statBoxTestEnhanced.SetBackgroundColour(GREY)
	statBoxTestEnhanced.SetForegroundColour(BLACK)
        statBoxSizer = wx.StaticBoxSizer(statBoxTestEnhanced, wx.VERTICAL)

        statBoxSizer.Add(paramSizer1, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 10)
        statBoxSizer.Add(paramSizer2, 0, wx.BOTTOM|wx.LEFT, 15)
        statBoxSizer.Add(paramSizer3, 0, wx.BOTTOM|wx.LEFT, 15)

	return statBoxSizer

    def setup_test_run(self):

	bmpUp = wx.Bitmap("up.png", wx.BITMAP_TYPE_ANY)
	bmpDown = wx.Bitmap("up2.png", wx.BITMAP_TYPE_ANY)
	bmpStop = wx.Bitmap("stop.png", wx.BITMAP_TYPE_ANY)

        btnTestRunUp = wx.BitmapButton(self, wx.ID_ANY, bitmap=bmpUp)
        btnTestRunDown = wx.BitmapButton(self, wx.ID_ANY, bitmap=bmpDown)
        btnTestStop = wx.BitmapButton(self, wx.ID_ANY, bitmap=bmpStop)
        self.Bind(wx.EVT_BUTTON, self.onTestRunUp, btnTestRunUp)
        self.Bind(wx.EVT_BUTTON, self.onTestRunDown, btnTestRunDown)
        self.Bind(wx.EVT_BUTTON, self.onTestStop, btnTestStop)

        speed = wx.StaticText(self, wx.ID_ANY, 'Speed')

	spinCtrlSpeed = wx.SpinCtrl(self, value='0')
	spinCtrlSpeed.SetRange(0, 25)

	paramSizer1 = wx.BoxSizer(wx.VERTICAL)
	paramSizer1.Add(speed, 0, wx.LEFT, 30)
	paramSizer1.Add(spinCtrlSpeed, 0, wx.TOP, 10)

	paramSizer2 = wx.BoxSizer(wx.HORIZONTAL)
	paramSizer2.Add(btnTestRunUp, 0, wx.TOP|wx.LEFT, 10)
	paramSizer2.Add(btnTestRunDown, 0, wx.TOP|wx.LEFT, 10)
	paramSizer2.Add(btnTestStop, 0, wx.TOP|wx.LEFT, 10)

	statBoxTestRun = wx.StaticBox(self, wx.ID_ANY, '  Test Run')
	statBoxTestRun.SetBackgroundColour(GREY)
	statBoxTestRun.SetForegroundColour(BLACK)
        statBoxSizer = wx.StaticBoxSizer(statBoxTestRun, wx.HORIZONTAL)

        statBoxSizer.Add(paramSizer1, 0, wx.ALL, 10)
        statBoxSizer.Add(paramSizer2, 0, wx.ALL, 10)

	return statBoxSizer

    def setup_multi_text_control(self):

        headline = '       - ACX/TCX logging - \n'
	txtMultiCtrl = wx.TextCtrl(self, -1, headline, size=(790, 180), style=wx.TE_MULTILINE)
        txtMultiCtrl.SetInsertionPoint(0)

	return txtMultiCtrl

    def onConnect(self, event):
	print 'Connect'

    def onConfigure(self, event):
	print 'Configure'

    def lock_text_controls(self):
        self.txtCtrl_cl_max.Disable()
        self.txtCtrl_cl_min.Disable()
        self.txtCtrl_sl_ki.Disable()
        self.txtCtrl_sl_max.Disable()
        self.txtCtrl_sl_min.Disable()
        self.txtCtrl_has_switch.Disable()
        self.txtCtrl_power_margin.Disable()
        self.txtCtrl_power_factor.Disable()
        self.txtCtrl_brightness_lo.Disable()
        self.txtCtrl_brake_temp_ok.Disable()
        self.txtCtrl_brake_temp_hi.Disable()
        self.txtCtrl_brake_max_id.Disable()
        self.txtCtrl_brake_pos_ratio.Disable()
        self.txtCtrl_trajec_acc.Disable()
        self.txtCtrl_trajec_ret.Disable()
        self.txtCtrl_dominant_throttle_on.Disable()
        self.txtCtrl_max_motor_temp.Disable()
        self.txtCtrl_num_motor_ch.Disable()
        self.txtCtrl_idle_timeout.Disable()
        self.txtCtrl_rope_stuck_on.Disable()
        self.txtCtrl_iq_alpha.Disable()
        self.txtCtrl_speed_alpha.Disable()
        self.txtCtrl_undershoot.Disable()
        self.txtCtrl_delay_start.Disable()
        
    def onTestInject(self, event):
	print 'Test Inject'

    def onGetIq(self, event):
	print 'Get iq'

    def onSaveParam(self, event):
	print 'Save param'

    def onTestRunUp(self, event):
	print 'Test run Up'
        serial_cmd('e', self.dl.ser)

    def onTestRunDown(self, event):
	print 'Test run Down'

    def onTestStop(self, event):
	print 'Test stop'

    def onCombo(self, event):
        print 'Selected port: '
