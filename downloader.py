import wx
import serial
import logging
from wx.lib.pubsub import pub
from wx.lib.pubsub import setupkwargs

GREY  = (180, 180, 180)
BLACK = (0, 0, 0)
TEXT_SERIAL_PORT_BORDER = 10

PARAMETER_NAMES = ['motor.cl.max', 'motor.cl.min', 'motor.sl.ki', 'motor.sl.max', 'motor.sl.min', \
                   'throttle.has_switch', 'power_margin', 'power_factor', 'led.brightness_lo', 'brake_temp_ok', \
		   'brake_temp_hi', 'brake_max_id', 'brake_test.pos_ratio', 'trajec.acc', 'trajec.ret', \
		   'dominant_throttle_on', 'max_motor_temp', 'num_motor_ch', 'idle_timeout']

def serial_cmd(cmd, serial):
    # send command to serial port
    try:
        serial.write(cmd + '\r');
    except:
        print 'Not Connected!'

class DownLoaderForm(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

	self.ser = None

	downloadSizer = self.setup_serial_sizer()
	versionSizer = self.setup_version_sizer()
	configSizer = self.setup_config_sizer()

	self.connected = False # flag indicating if connection to serial port is established
#
        topSizer = wx.BoxSizer(wx.VERTICAL)
	topSizer.Add(downloadSizer, 0, wx.TOP|wx.LEFT, 10)
	topSizer.Add(versionSizer, 0, wx.TOP|wx.LEFT, 10)
	topSizer.Add(configSizer, 0, wx.TOP|wx.LEFT, 10)
        self.SetSizer(topSizer)

	pub.subscribe(self.configListener, 'configListener')
	pub.subscribe(self.serialListener, 'serialListener')
        logging.basicConfig(format="%(funcName)s() - %(message)s", level=logging.INFO)

    def serialListener(self, message, fname=None):
        logging.info('')
	self.mySer = message

    def configListener(self, message, fname=None):
        """
            Handle configuration data read from 'Open'.
	"""
        logging.info('File name: %s', fname)
	self.configParameters = message
	self.configurationFileName = fname

    def print_parameters(self):
        """
            Update filename in Configuration sizer.
	    Then extract parameters.
	"""
        logging.info('')
	self.txtFileName.SetLabel(self.configurationFileName)
	#print self.configParameters
	self.config_parameters()

    def config_parameters(self):
        """
            Configure parameters via serial IF.
	    Parameters are configured when file is read.
	"""
	parListLength = len(self.configParameters)
        logging.info('Par list length: %s', parListLength)

	for parIndex in range(0, parListLength):
	    par1 = self.configParameters[parIndex]
	    par2 = par1.split(',')
	    par3 = par2[1].strip('\n')
            local_cmd = 'param set' + PARAMETER_NAMES + par3
	    print local_cmd

        #serial_cmd(local_cmd, self.mySer)

    def setup_serial_sizer(self):
        txtSerialPort = wx.StaticText(self, wx.ID_ANY, 'Select serial port')
	txtSerPortSizer = wx.BoxSizer(wx.HORIZONTAL)
	txtSerPortSizer.Add(txtSerialPort, 0, wx.TOP, TEXT_SERIAL_PORT_BORDER)

        portNames = ['ACM0', 'ACM1', 'USB0']
        self.comboBox = wx.ComboBox(self, choices=portNames)
        self.comboBox.SetSelection(0) # preselect ACM0
        self.comboBox.Bind(wx.EVT_COMBOBOX, self.onCombo)

	comboSizer = wx.BoxSizer(wx.HORIZONTAL)
	comboSizer.Add(self.comboBox, 0, wx.TOP, 10)

	statBoxSerial = wx.StaticBox(self, wx.ID_ANY, '  Serial connection    ')
	statBoxSerial.SetBackgroundColour(GREY)
	statBoxSerial.SetForegroundColour(BLACK)
        statBoxSizer = wx.StaticBoxSizer(statBoxSerial, wx.HORIZONTAL)

        btnConnect = wx.Button(self, wx.ID_ANY, 'Connect')
        self.Bind(wx.EVT_BUTTON, self.onConnect, btnConnect)
	self.lblConnect = wx.StaticText(self, label= 'Not connected')

        btnQuit = wx.Button(self, wx.ID_ANY, 'Quit')
	btnQuitSizer = wx.BoxSizer(wx.HORIZONTAL)
	btnQuitSizer.Add(btnQuit, 0, wx.ALL, 20)

        statBoxSizer.Add(txtSerPortSizer, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 15)
        statBoxSizer.Add(comboSizer, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 10)
        statBoxSizer.Add(btnConnect, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 20)
        statBoxSizer.Add(self.lblConnect, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 25)
        statBoxSizer.Add(btnQuitSizer, 0, wx.LEFT, 420)

	return statBoxSizer

    def setup_version_sizer(self):
	statBoxDownload = wx.StaticBox(self, wx.ID_ANY, '  Version')
	statBoxDownload.SetBackgroundColour(GREY)
	statBoxDownload.SetForegroundColour(BLACK)
        statBoxSizer = wx.StaticBoxSizer(statBoxDownload, wx.VERTICAL)

        txtNull = wx.StaticText(self, wx.ID_ANY, ' ')

        ascenderVersion = wx.StaticText(self, -1, "Ascender Version:")
        remoteVersion = wx.StaticText(self, -1, "Remote Version:")

        btnDownload = wx.Button(self, wx.ID_ANY, 'Download')
        self.Bind(wx.EVT_BUTTON, self.onDownload, btnDownload)

        statBoxSizer.Add(btnDownload, 0, wx.ALL, 20)
        statBoxSizer.Add(ascenderVersion, 0, wx.ALL, 20)
        statBoxSizer.Add(txtNull, 0, wx.LEFT, 1000)
        statBoxSizer.Add(remoteVersion, 0, wx.ALL, 20)

	return statBoxSizer

    def setup_config_sizer(self):
	statBoxDownload = wx.StaticBox(self, wx.ID_ANY, '  Configuration')
	statBoxDownload.SetBackgroundColour(GREY)
	statBoxDownload.SetForegroundColour(BLACK)
        statBoxSizer = wx.StaticBoxSizer(statBoxDownload, wx.VERTICAL)

        txtNull = wx.StaticText(self, wx.ID_ANY, ' ')

        self.txtConfiguration = wx.StaticText(self, -1, "Configuration file:")
        self.txtFileName = wx.StaticText(self, -1, "No file name selected")

	configSizer = wx.BoxSizer(wx.HORIZONTAL)
        configSizer.Add(self.txtConfiguration, 0, wx.TOP|wx.LEFT, 10)
        configSizer.Add(self.txtFileName, 0, wx.TOP|wx.LEFT, 10)

        btnConfig= wx.Button(self, wx.ID_ANY, 'Config')
        self.Bind(wx.EVT_BUTTON, self.onConfig, btnConfig)

        statBoxSizer.Add(configSizer, 0, wx.ALL, 15)
        statBoxSizer.Add(btnConfig, 0, wx.ALL, 15)
        statBoxSizer.Add(txtNull, 0, wx.LEFT, 1000)

	return statBoxSizer

    def onConnect(self, event):
        logging.info('Downloder connected to: %s', self.comboBox.GetValue())

	try:
	    self.connected = True
            self.ser = serial.Serial(port = '/dev/tty'+self.comboBox.GetValue(),
                                     baudrate = 9600,
                                     parity = serial.PARITY_NONE,
                                     stopbits = serial.STOPBITS_ONE,
                                     bytesize = serial.EIGHTBITS,
                                     timeout = 1)

            self.lblConnect.SetForegroundColour(wx.Colour(11, 102 , 66))
	    self.lblConnect.SetLabel("Connected to " + self.comboBox.GetValue())

	except:
            self.lblConnect.SetForegroundColour(wx.Colour(255,0,0))
	    self.lblConnect.SetLabel('Cannot connect')

	pub.sendMessage('serialListener', message=self.ser)

    def onDownload(self, event):
        logging.info('')
	print_const()

    def onCombo(self, event):
        print 'Selected port: '

    def onConfig(self, event):
        logging.info('')
	print self.configParameters

