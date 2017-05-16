# Author      : Heinz Samuelsson
# Date        : ons 10 maj 2017 10:00:55 CEST
# File        : param_setting2.py
# Reference   : -
# Description : Application is used to set parameters for ActSafe's
#               Ascender ACX and TCX.
import wx
import time

BORDER1 = 5
BORDER2 = 3
GREEN = (0, 255, 0)
INJECT_COLOR = (200, 160, 100)

class MyForm(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title='Parameter Setting', size=(1000,500))
        self.panel = wx.Panel(self, wx.ID_ANY, style=wx.RAISED_BORDER)

	#self.Centre()
	self.SetPosition((2500, 480))

        self.connectBtn = wx.Button(self.panel, wx.ID_ANY, 'Connect')
	self.lblConnected = wx.StaticText(self.panel, label= 'Not connected')

        #self.configBtn = wx.Button(self.panel, wx.ID_ANY, 'Config')
        self.testInjectBtn = wx.Button(self.panel, wx.ID_ANY, 'Test Inject')
        self.getIqBtn = wx.Button(self.panel, wx.ID_ANY, 'get_iq')
        self.quitBtn = wx.Button(self.panel, wx.ID_ANY, 'Quit')

	self.defineCombo()

        self.param_cl_kp = wx.StaticText(self.panel, wx.ID_ANY, 'param.cl.kp')
        self.param_cl_ki = wx.StaticText(self.panel, wx.ID_ANY, 'param.cl.ki')
        self.param_sl_kp = wx.StaticText(self.panel, wx.ID_ANY, 'param.sl.kp')
        self.param_sl_ki = wx.StaticText(self.panel, wx.ID_ANY, 'param.sl.ki')
        self.param_throttle_zero = wx.StaticText(self.panel, wx.ID_ANY, 'param.throttle_zero')
        self.param_throttle_down = wx.StaticText(self.panel, wx.ID_ANY, 'param.throttle_down')
        self.param_throttle_up = wx.StaticText(self.panel, wx.ID_ANY, 'param.throttle_up')
        self.param_throttle_deadband_on = wx.StaticText(self.panel, wx.ID_ANY, 'param.throttle_deadband_on')
        self.param_dominant_throttle_on = wx.StaticText(self.panel, wx.ID_ANY, 'param.dominant_throttle_on')
        self.param_rope_stuck_on = wx.StaticText(self.panel, wx.ID_ANY, 'param.rope_stuck_on')
        self.param_iq_alpha = wx.StaticText(self.panel, wx.ID_ANY, 'param.iq_alpha')

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

	self.paramSizer1 = wx.BoxSizer(wx.VERTICAL)
	self.paramSizer1.Add(self.param_cl_kp, 0, wx.ALL, BORDER1)
	self.paramSizer1.Add(self.txtCtrl_cl_kp, 0, wx.ALL, BORDER1)
	self.paramSizer1.Add(self.param_cl_ki, 0, wx.ALL, BORDER1)
	self.paramSizer1.Add(self.txtCtrl_cl_ki, 0, wx.ALL, BORDER1)
	self.paramSizer1.Add(self.param_sl_kp, 0, wx.ALL, BORDER1)
	self.paramSizer1.Add(self.txtCtrl_sl_kp, 0, wx.ALL, BORDER1)
	self.paramSizer1.Add(self.param_sl_ki, 0, wx.ALL, BORDER1)
	self.paramSizer1.Add(self.txtCtrl_sl_ki, 0, wx.ALL, BORDER1)

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

        self.Bind(wx.EVT_BUTTON, self.onConnect, self.connectBtn)
        self.Bind(wx.EVT_BUTTON, self.onTestInject, self.testInjectBtn)
        self.Bind(wx.EVT_BUTTON, self.onGetIq, self.getIqBtn)
        self.Bind(wx.EVT_BUTTON, self.onQuit, self.quitBtn)

        #box[i] = wx.StaticBox(panel, wx.ID_ANY, "testBox", size=(0,100))
	self.statBoxSerial = wx.StaticBox(self.panel, wx.ID_ANY, '  Serial connection    ', size=(0,20))
	self.statBoxSerial.SetBackgroundColour((180,180,180))
	self.statBoxSerial.SetForegroundColour((0,0,0))
        self.staticBoxSizer1 = wx.StaticBoxSizer(self.statBoxSerial, wx.HORIZONTAL)
        self.staticBoxSizer1.Add(self.combo, 0, wx.ALL, BORDER1)
	self.staticBoxSizer1.Add(self.connectBtn, 0, wx.ALL, BORDER1)
	self.staticBoxSizer1.Add(self.lblConnected, 0, wx.ALL, BORDER1)

	self.statBoxParams = wx.StaticBox(self.panel, wx.ID_ANY, '  Parameters   ')
	self.statBoxParams.SetBackgroundColour((180,180,180))
	self.statBoxParams.SetForegroundColour((0,0,0))
        self.staticBoxSizer2 = wx.StaticBoxSizer(self.statBoxParams, wx.HORIZONTAL)
	self.staticBoxSizer2.Add(self.paramSizer1, 0, wx.ALL, BORDER1)
	self.staticBoxSizer2.Add(self.paramSizer2, 0, wx.ALL, BORDER1)
	self.staticBoxSizer2.Add(self.paramSizer3, 0, wx.ALL, BORDER1)

	self.statBoxMisc = wx.StaticBox(self.panel, wx.ID_ANY, '  Debugging   ')
	self.statBoxMisc.SetBackgroundColour((180,180,180))
	self.statBoxMisc.SetForegroundColour((0,0,0))
        self.staticBoxSizer3 = wx.StaticBoxSizer(self.statBoxMisc, wx.HORIZONTAL)
	self.staticBoxSizer3.Add(self.testInjectBtn, 0, wx.ALL, BORDER1)
	self.staticBoxSizer3.Add(self.getIqBtn, 0, wx.ALL, BORDER1)
	self.staticBoxSizer3.Add(self.quitBtn, 0, wx.ALL, BORDER1)

        self.topSizer = wx.BoxSizer(wx.VERTICAL)
        self.topSizer.Add(self.staticBoxSizer1, 1, wx.ALL|wx.EXPAND, BORDER1)
        self.topSizer.Add(self.staticBoxSizer2, 1, wx.ALL|wx.EXPAND, BORDER1)
        self.topSizer.Add(self.staticBoxSizer3, 1, wx.ALL|wx.EXPAND, BORDER1)

        self.panel.SetSizer(self.topSizer)
        #self.topSizer.Fit(self)

    def onConnect(self, event):
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
	self.lblConnected.SetFont(font)
        self.lblConnected.SetForegroundColour(wx.Colour(11, 102 , 66))
        self.lblConnected.SetLabel('Connected to tty' + self.combo.GetValue())

    def defineCombo(self):
        portNames = ['ACM0', 'ACM1', 'USB0']
        self.combo = wx.ComboBox(self.panel, choices=portNames, pos=(140, 27))
        self.combo.SetSelection(0) # preselect ACM0
        self.combo.Bind(wx.EVT_COMBOBOX, self.onCombo)

    def onConfig(self, event):
        print 'Config'

    def onTestInject(self, event):
        print 'Test inject'

    def onGetIq(self, event):
        print 'get_iq'

    def onCombo(self, event):
        print 'Selected port: ' + self.combo.GetValue()

    def onQuit(self, event):
        self.Close()



if __name__ == '__main__':
    app = wx.App()
    frame = MyForm().Show()
    app.MainLoop()
