#!/usr/bin/python

import wx
import time

WINDOW_SIZE = (1035, 770)

# sizer borders
BORDER1 = 5
TEXT_SERIAL_PORT_BORDER = 10

HEADLINE = 'Production Test Tool, Ascender ACX/TCX'

# color codes
GREY    = (180, 180, 180)
BLACK   = (0, 0, 0)

class SerialSizer():
    pass

class MyForm(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title=HEADLINE, style=wx.DEFAULT_FRAME_STYLE, size=WINDOW_SIZE)
        self.panel = wx.Panel(self, wx.ID_ANY, style=wx.BORDER_RAISED)

	#self.Centre()
	self.SetPosition((2500, 100))

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

        self.panel.SetSizer(topSizer)

    def setup_serial_sizer(self):
        txtSerialPort = wx.StaticText(self.panel, wx.ID_ANY, 'Select serial port')
	txtSerPortSizer = wx.BoxSizer(wx.HORIZONTAL)
	txtSerPortSizer.Add(txtSerialPort, 0, wx.TOP, TEXT_SERIAL_PORT_BORDER)

        portNames = ['ACM0', 'ACM1', 'USB0']
        comboBox = wx.ComboBox(self.panel, choices=portNames)
        comboBox.SetSelection(0) # preselect ACM0
        comboBox.Bind(wx.EVT_COMBOBOX, self.onCombo)
	comboSizer = wx.BoxSizer(wx.HORIZONTAL)
	comboSizer.Add(comboBox, 0, wx.TOP, 10)

	statBoxSerial = wx.StaticBox(self.panel, wx.ID_ANY, '  Serial connection    ')
	statBoxSerial.SetBackgroundColour(GREY)
	statBoxSerial.SetForegroundColour(BLACK)
        statBoxSizer = wx.StaticBoxSizer(statBoxSerial, wx.HORIZONTAL)

        btnConnect = wx.Button(self.panel, wx.ID_ANY, 'Connect')
        self.Bind(wx.EVT_BUTTON, self.onConnect, btnConnect)
	lblConnect = wx.StaticText(self.panel, label= 'Not connected')

        btnQuit = wx.Button(self.panel, wx.ID_ANY, 'Quit')
	btnQuitSizer = wx.BoxSizer(wx.HORIZONTAL)
	btnQuitSizer.Add(btnQuit, 0, wx.ALL, 20)
        self.Bind(wx.EVT_BUTTON, self.onQuit, btnQuit)

        statBoxSizer.Add(txtSerPortSizer, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 15)
        statBoxSizer.Add(comboSizer, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 10)
        statBoxSizer.Add(btnConnect, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 20)
        statBoxSizer.Add(lblConnect, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 25)
        statBoxSizer.Add(btnQuitSizer, 0, wx.LEFT, 420)

	return statBoxSizer

    def setup_config_params(self):

        param_cl_max = wx.StaticText(self.panel, wx.ID_ANY, 'cl.max')
        txtCtrl_cl_max = wx.TextCtrl(self.panel, wx.ID_ANY,'51.00')
        param_cl_min = wx.StaticText(self.panel, wx.ID_ANY, 'cl.min')
        txtCtrl_cl_min = wx.TextCtrl(self.panel, wx.ID_ANY,'-51.00')
        param_sl_max = wx.StaticText(self.panel, wx.ID_ANY, 'sl.max')
        txtCtrl_sl_max = wx.TextCtrl(self.panel, wx.ID_ANY,'80.00')
        param_sl_min = wx.StaticText(self.panel, wx.ID_ANY, 'sl.min')
        txtCtrl_sl_min = wx.TextCtrl(self.panel, wx.ID_ANY,'-80.00')

	paramSizer1 = wx.BoxSizer(wx.VERTICAL)
	paramSizer1.Add(param_cl_max, 0, wx.TOP, 10)
	paramSizer1.Add(txtCtrl_cl_max, 0, wx.TOP, 10)
	paramSizer1.Add(param_cl_min, 0, wx.TOP, 10)
	paramSizer1.Add(txtCtrl_cl_min, 0, wx.TOP, 10)

	paramSizer2 = wx.BoxSizer(wx.VERTICAL)
	paramSizer2.Add(param_sl_max, 0, wx.TOP, 10)
	paramSizer2.Add(txtCtrl_sl_max, 0, wx.TOP, 10)
	paramSizer2.Add(param_sl_min, 0, wx.TOP, 10)
	paramSizer2.Add(txtCtrl_sl_min, 0, wx.TOP, 10)

	statBoxConfigParams = wx.StaticBox(self.panel, wx.ID_ANY, '  Set paramters')
	statBoxConfigParams.SetBackgroundColour(GREY)
	statBoxConfigParams.SetForegroundColour(BLACK)
        statBoxSizer = wx.StaticBoxSizer(statBoxConfigParams, wx.HORIZONTAL)

        statBoxSizer.Add(paramSizer1, 0, wx.ALL, 10)
        statBoxSizer.Add(paramSizer2, 0, wx.ALL, 10)

	return statBoxSizer

    def setup_test_enahanced_measuring(self):

        param_rope_stuck_on = wx.StaticText(self.panel, wx.ID_ANY, 'rope_stuck_on')
        txtCtrl_rope_stuck_on = wx.TextCtrl(self.panel, wx.ID_ANY,'1')
        param_iq_alpha = wx.StaticText(self.panel, wx.ID_ANY, 'iq_alpha')
        txtCtrl_iq_alpha = wx.TextCtrl(self.panel, wx.ID_ANY,'0.005')
        param_speed_alpha = wx.StaticText(self.panel, wx.ID_ANY, 'speed_alpha')
        txtCtrl_speed_alpha = wx.TextCtrl(self.panel, wx.ID_ANY,'0.05')
        param_undershoot = wx.StaticText(self.panel, wx.ID_ANY, 'undershoot')
        txtCtrl_undershoot = wx.TextCtrl(self.panel, wx.ID_ANY,'-1.0')
        param_delay_start = wx.StaticText(self.panel, wx.ID_ANY, 'delay_start')
        txtCtrl_delay_start = wx.TextCtrl(self.panel, wx.ID_ANY,'5000')

        btnConfigure = wx.Button(self.panel, wx.ID_ANY, ' Configure   ')
        self.Bind(wx.EVT_BUTTON, self.onConfigure, btnConfigure)
        btnTestInject = wx.Button(self.panel, wx.ID_ANY, ' Test Inject ')
        self.Bind(wx.EVT_BUTTON, self.onTestInject, btnTestInject)
        btnGetIq = wx.Button(self.panel, wx.ID_ANY, '    Get iq          ')
        self.Bind(wx.EVT_BUTTON, self.onGetIq, btnGetIq)
        btnSaveParam = wx.Button(self.panel, wx.ID_ANY, ' SaveParam ')
        self.Bind(wx.EVT_BUTTON, self.onSaveParam, btnSaveParam)

	paramSizer1 = wx.BoxSizer(wx.HORIZONTAL)
	paramSizer1.Add(param_rope_stuck_on, 0, wx.LEFT, 10)
	paramSizer1.Add(param_iq_alpha, 0, wx.LEFT, 14)
	paramSizer1.Add(param_speed_alpha, 0, wx.LEFT, 44)
	paramSizer1.Add(param_undershoot, 0, wx.LEFT, 24)
	paramSizer1.Add(param_delay_start, 0, wx.LEFT, 24)

	paramSizer2 = wx.BoxSizer(wx.HORIZONTAL)
	paramSizer2.Add(txtCtrl_rope_stuck_on, 0, wx.RIGHT, 10)
	paramSizer2.Add(txtCtrl_iq_alpha, 0, wx.LEFT, 15)
	paramSizer2.Add(txtCtrl_speed_alpha, 0, wx.LEFT, 15)
	paramSizer2.Add(txtCtrl_undershoot, 0, wx.LEFT, 15)
	paramSizer2.Add(txtCtrl_delay_start, 0, wx.LEFT, 15)

	paramSizer3 = wx.BoxSizer(wx.HORIZONTAL)
	paramSizer3.Add(btnConfigure, 0, wx.RIGHT, 10)
	paramSizer3.Add(btnTestInject, 0, wx.LEFT, 15)
	paramSizer3.Add(btnGetIq, 0, wx.LEFT, 15)
	paramSizer3.Add(btnSaveParam, 0, wx.LEFT, 15)

	statBoxTestEnhanced = wx.StaticBox(self.panel, wx.ID_ANY, '  Test Enhanced Measuring')
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

        btnTestRunUp = wx.BitmapButton(self.panel, wx.ID_ANY, bitmap=bmpUp)
        btnTestRunDown = wx.BitmapButton(self.panel, wx.ID_ANY, bitmap=bmpDown)
        btnTestStop = wx.BitmapButton(self.panel, wx.ID_ANY, bitmap=bmpStop)
        self.Bind(wx.EVT_BUTTON, self.onTestRunUp, btnTestRunUp)
        self.Bind(wx.EVT_BUTTON, self.onTestRunDown, btnTestRunDown)
        self.Bind(wx.EVT_BUTTON, self.onTestStop, btnTestStop)

        speed = wx.StaticText(self.panel, wx.ID_ANY, 'Speed')

	spinCtrlSpeed = wx.SpinCtrl(self.panel, value='0')
	spinCtrlSpeed.SetRange(0, 25)

	paramSizer1 = wx.BoxSizer(wx.VERTICAL)
	paramSizer1.Add(speed, 0, wx.LEFT, 30)
	paramSizer1.Add(spinCtrlSpeed, 0, wx.TOP, 10)

	paramSizer2 = wx.BoxSizer(wx.HORIZONTAL)
	paramSizer2.Add(btnTestRunUp, 0, wx.TOP|wx.LEFT, 10)
	paramSizer2.Add(btnTestRunDown, 0, wx.TOP|wx.LEFT, 10)
	paramSizer2.Add(btnTestStop, 0, wx.TOP|wx.LEFT, 10)

	statBoxTestRun = wx.StaticBox(self.panel, wx.ID_ANY, '  Test Run')
	statBoxTestRun.SetBackgroundColour(GREY)
	statBoxTestRun.SetForegroundColour(BLACK)
        statBoxSizer = wx.StaticBoxSizer(statBoxTestRun, wx.HORIZONTAL)

        statBoxSizer.Add(paramSizer1, 0, wx.ALL, 10)
        statBoxSizer.Add(paramSizer2, 0, wx.ALL, 10)

	return statBoxSizer

    def setup_multi_text_control(self):

        headline = '       - ACX/TCX logging - \n'
	txtMultiCtrl = wx.TextCtrl(self.panel, -1, headline, size=(790, 180), style=wx.TE_MULTILINE)
        txtMultiCtrl.SetInsertionPoint(0)

	return txtMultiCtrl

    def onConnect(self, event):
	print 'Connect'

    def onConfigure(self, event):
	print 'Configure'

    def onTestInject(self, event):
	print 'Test Inject'

    def onGetIq(self, event):
	print 'Get iq'

    def onSaveParam(self, event):
	print 'Save param'

    def onTestRunUp(self, event):
	print 'Test run Up'

    def onTestRunDown(self, event):
	print 'Test run Down'

    def onTestStop(self, event):
	print 'Test stop'

    def onCombo(self, event):
        print 'Selected port: '

    def onQuit(self, event):
        rv = self.exitDialog.ShowModal()

        if rv == wx.ID_YES:
            self.Close(True)


if __name__ == '__main__':
    app = wx.App()
    frame = MyForm().Show()
    app.MainLoop()
