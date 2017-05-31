import wx

GREY  = (180, 180, 180)
BLACK = (0, 0, 0)

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

        txtThrottleMaxUp = wx.StaticText(self, wx.ID_ANY, 'Turn throttle handle max up')
        txtThrottleMaxDown = wx.StaticText(self, wx.ID_ANY, 'Turn throttle handle max down')
        txtThrottleNeutral = wx.StaticText(self, wx.ID_ANY, 'Set throttle handle in neutal position')
        txtNull = wx.StaticText(self, wx.ID_ANY, ' ')

        btnCalibRight = wx.Button(self, wx.ID_ANY, 'Calib Right')
        btnCalibLeft = wx.Button(self, wx.ID_ANY, 'Calib Left')
        btnCalibNeutral = wx.Button(self, wx.ID_ANY, 'Calib Neutral')
        btnCalibRestart = wx.Button(self, wx.ID_ANY, 'Calib Restart')

	rightSizer = wx.BoxSizer(wx.HORIZONTAL)
        rightSizer.Add(btnCalibRight, 0, wx.TOP|wx.LEFT, 10)
        rightSizer.Add(txtThrottleMaxUp, 0, wx.TOP|wx.LEFT, 15)

	leftSizer = wx.BoxSizer(wx.HORIZONTAL)
        leftSizer.Add(btnCalibLeft, 0, wx.TOP|wx.LEFT, 10)
        leftSizer.Add(txtThrottleMaxDown, 0, wx.TOP|wx.LEFT, 15)

	neutralSizer = wx.BoxSizer(wx.HORIZONTAL)
        neutralSizer.Add(btnCalibNeutral, 0, wx.TOP|wx.LEFT, 10)
        neutralSizer.Add(txtThrottleNeutral, 0, wx.TOP|wx.LEFT, 15)

        statBoxSizer.Add(rightSizer, 0, wx.ALL, 10)
        statBoxSizer.Add(leftSizer, 0, wx.ALL, 10)
        statBoxSizer.Add(neutralSizer, 0, wx.ALL, 10)
        statBoxSizer.Add(btnCalibRestart, 0, wx.TOP|wx.LEFT, 20)
        statBoxSizer.Add(txtNull, 0, wx.LEFT, 1000) # this is just to get the statBoxSerial larger 

	return statBoxSizer

    def setup_save_param_sizer(self):
	statBoxSerial = wx.StaticBox(self, wx.ID_ANY, '  Save Parameter')
	statBoxSerial.SetBackgroundColour(GREY)
	statBoxSerial.SetForegroundColour(BLACK)
        statBoxSizer = wx.StaticBoxSizer(statBoxSerial, wx.HORIZONTAL)
        txtNull = wx.StaticText(self, wx.ID_ANY, ' ')

        btnSaveParam = wx.Button(self, wx.ID_ANY, 'Save Param')
        statBoxSizer.Add(btnSaveParam, 0, wx.ALL, 20)
        statBoxSizer.Add(txtNull, 0, wx.LEFT, 870) # this is just to get the statBoxSerial larger 

	return statBoxSizer

    def onAlign(self, event):
        print 'Align'
        #wx.CallAfter(Publisher.sendMessage, "topic_aligned", "Aligned done")
