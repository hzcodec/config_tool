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

	self.leftTopSizer = wx.BoxSizer(wx.VERTICAL)
        self.leftTopSizer.Add(serialSizer, 0, wx.ALL|wx.EXPAND, BORDER1)
        self.leftTopSizer.Add(configParamsSizer, 0, wx.ALL|wx.EXPAND, BORDER1)
        self.leftTopSizer.Add(enhancedMeasSizer, 0, wx.ALL|wx.EXPAND, BORDER1)
        self.topSizer = wx.BoxSizer(wx.HORIZONTAL)
	self.topSizer.Add(self.leftTopSizer, 0, wx.ALL, BORDER1)

        self.panel.SetSizer(self.topSizer)

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

	statBoxTestEnhanced = wx.StaticBox(self.panel, wx.ID_ANY, '  Test Enhanced Measuring')
	statBoxTestEnhanced.SetBackgroundColour(GREY)
	statBoxTestEnhanced.SetForegroundColour(BLACK)
        statBoxSizer = wx.StaticBoxSizer(statBoxTestEnhanced, wx.VERTICAL)

        statBoxSizer.Add(paramSizer1, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 10)
        statBoxSizer.Add(paramSizer2, 0, wx.BOTTOM|wx.LEFT, 15)

	return statBoxSizer


    def onConnect(self, event):
	print 'Connect'
    

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
