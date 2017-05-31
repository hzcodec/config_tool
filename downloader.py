import wx
import serial
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub as Publisher

GREY  = (180, 180, 180)
BLACK = (0, 0, 0)
TEXT_SERIAL_PORT_BORDER = 10

class DownLoaderForm(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

	self.ser = None

	downloadSizer = self.setup_serial_sizer()
	versionSizer = self.setup_version_sizer()

	self.connected = False # flag indicating if connection to serial port is established

        topSizer = wx.BoxSizer(wx.VERTICAL)
	topSizer.Add(downloadSizer, 0, wx.TOP|wx.LEFT, 10)
	topSizer.Add(versionSizer, 0, wx.TOP|wx.LEFT, 10)
        self.SetSizer(topSizer)

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

    def onConnect(self, event):
        print 'Connect:', self.comboBox.GetValue()

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

	Publisher.sendMessage(('show.data'), data=self.ser)

    def connectionOK(self, msg):
        print 'connectionOK'

    def onDownload(self, event):
        print 'Download'
	print_const()

    def onCombo(self, event):
        print 'Selected port: '

