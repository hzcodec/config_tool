# Auther      : Heinz Samuelsson
# Date        : 2017-06-02
# File        : downloader.py, part of prod_test_tool.py
# Reference   : -
# Description : Remember to set gauge size according to the length of parameter list.
#               Right now the length is: range = 18
#               The length is extracted in config_parameters() function.
#               Also the PARAMETER_NAMES need to be updated.
#
# Python ver  : 2.7.3 (gcc 4.6.3)

import wx
import serial
import logging
import time
from wx.lib.pubsub import pub
from wx.lib.pubsub import setupkwargs

# motor.cl.kp: 0.229996
# motor.cl.ki: 0.030518
# motor.cl.kt: 1.000000
# motor.cl.max: 51.000000
# motor.cl.min: -51.000000

# motor.sl.kp: 15.000000
# motor.sl.ki: 0.250000
# motor.sl.kt: 0.125000
# motor.sl.max: 80.000000
# motor.sl.min: -80.000000

# trajec.acc: 80.000000
# trajec.ret: 320.000000
# throttle.zero: 0.501099
# throttle.down: 0.328705
# throttle.up: 0.672745

# throttle.deadband_on: 0.030518
# throttle.deadband_off: 0.027466
# throttle.has_switch: 1
# num_motor_ch: 1

# power_out: 300.000000
# power_in: 100.000000
# brake_temp_ok: 60.000000
# brake_temp_hi: 65.000000
# brake_max_id: 40.000000

# angle_offset: 0.473084
# alignment_current: 40.000000

# sin_bias: 0.050049
# sin_gain: 4.946854
# cos_bias: 0.051147
# cos_gain: 4.949844

# brake_test.pos_ratio: 0.399994
# brake_test.neg_ratio: 0.199997
# psu_ok: 0
# led.brightness_hi: 0.300003
# led.brightness_lo: 0.300003

# idreg.kp: 0.009995
# idreg.ki: 0.001007
# idreg.kt: 0.500000
# power_margin: 0.000000
# power_factor: 1.000000

# speed_filter: 2147483
# max_motor_temp: 100.000000
# idle_timeout: 14400
# remote_ctrl_timeout: 10
# soc_lim_run_up: 8

# max_drive_temp: 85.000000
# dominant_throttle_on: 1
# rope_stuck_on: 1
# iq_alpha: 0.005005
# speed_alpha: 0.050003

# mx: 40.000000
# mi: -39.999984
# delay_start: 5000
# speed_lim: 5.000000
# undershoot: -0.999985
# ti: 0

GREY  = (180, 180, 180)
BLACK = (0, 0, 0)
TEXT_SERIAL_PORT_BORDER = 10

# current parameters
PARAMETER_NAMES = ['motor.cl.kp', 'motor.cl.ki', 'motor.cl.kt', 'motor.cl.max', 'motor.cl.min', \
                   'motor.sl.kp', 'motor.sl.ki', 'motor.sl.kt', 'motor.sl.max', 'motor.sl_min', \
		   'trajec.acc', 'trajec.ret', 'throttle_zero', 'throttle_down', 'throttle_up' \
		   'throttle_deadband_on', 'throttle_deadband_off', 'throttle_has_switch', 'num_motor_ch', \
		   'power_out', 'power_in', 'brake_temp_ok', 'brake_temp_hi', 'brake_max_id', \
		   'angle_offset', 'alignment_current', \ 
		   'sin_bias', 'sin_gain', 'cos_bias', 'cos_gain', \
		   'brake_test.pos_ratio', 'brake_test.net_ratio', 'psu_ok', 'led.brightness_hi', 'led.brightness_lo'\
		   'idreg.kp', 'idreg.ki', 'idreg.kit', 'power_margin', 'power_factor', \
		   'speed_filter', 'max_motor_temp', 'idle_timeout', 'remote_ctrl_timeout', 'sock_lim_run_up', \
		   'max_drive_temp', 'dominant_throttle_on', 'rope_stuck_on', 'iq_alpha', 'speed_alpha', \
		   'mx', 'mi', 'delay_start', 'speed_lim', 'undershoot', 'ti']

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


class DownLoaderForm(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

	self.ser = None

	downloadSizer = self.setup_serial_sizer()
	versionSizer = self.setup_version_sizer()
	configSizer = self.setup_config_sizer()

	self.connected = False # flag indicating if connection to serial port is established

        topSizer = wx.BoxSizer(wx.VERTICAL)
	topSizer.Add(downloadSizer, 0, wx.TOP|wx.LEFT, 10)
	topSizer.Add(versionSizer, 0, wx.TOP|wx.LEFT, 10)
	topSizer.Add(configSizer, 0, wx.TOP|wx.LEFT, 10)
        self.SetSizer(topSizer)

	pub.subscribe(self.configListener, 'configListener')
	pub.subscribe(self.serialListener, 'serialListener')
        logging.basicConfig(format="%(funcName)s() - %(message)s", level=logging.INFO)

    def get_version(self):
        self.ascenderVersion = serial_read('v', 56, self.mySer)
        logging.info('Ascender version: %s', self.ascenderVersion) 

	aVersion = self.ascenderVersion.split("v")
	self.lblAscenderVersion.SetLabel(aVersion[1])

        self.remoteVersion = serial_read('r_v', 56, self.mySer)
        logging.info('Remote version: %s', self.remoteVersion) 
	rVersion = self.remoteVersion.split("r_v")
	self.lblRemoteVersion.SetLabel(rVersion[1])
 
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
	self.config_parameters()

    def config_parameters(self):
        """
            Configure parameters via serial IF.
	    Parameters are configured when file is selected via Open.
	    Save param button is disabled during configuration.
	"""
	self.btnSaveParam.Enable(False)
	parListLength = len(self.configParameters)
        logging.info('Par list length: %s', parListLength)
	self.txtFileName.SetLabel(self.configurationFileName)

	# get all parameters and its corresponding command
	for parIndex in range(0, parListLength):
	    par1 = self.configParameters[parIndex]
	    par2 = par1.split(',')
	    par3 = par2[1].strip('\n')
            local_cmd = 'param set ' + PARAMETER_NAMES[parIndex] + par3

	    print local_cmd
            #serial_cmd(local_cmd, self.mySer)
            time.sleep(0.3)
	    self.gauge.SetValue(parIndex)
	    wx.Yield()

	self.btnSaveParam.Enable(True)

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

        txtNull = wx.StaticText(self, wx.ID_ANY, ' ')

        statBoxSizer.Add(txtSerPortSizer, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 15)
        statBoxSizer.Add(comboSizer, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 10)
        statBoxSizer.Add(btnConnect, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 20)
        statBoxSizer.Add(self.lblConnect, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 25)
        statBoxSizer.Add(txtNull, 0, wx.LEFT, 545) # this is just to get the statBoxSerial larger 

	return statBoxSizer

    def setup_version_sizer(self):
	statBoxDownload = wx.StaticBox(self, wx.ID_ANY, '  Version')
	statBoxDownload.SetBackgroundColour(GREY)
	statBoxDownload.SetForegroundColour(BLACK)
        statBoxSizer = wx.StaticBoxSizer(statBoxDownload, wx.VERTICAL)

        txtNull  = wx.StaticText(self, wx.ID_ANY, ' ')
        txtNull2 = wx.StaticText(self, wx.ID_ANY, ' ')

        ascenderVersionHeadline = wx.StaticText(self, -1, "Ascender Version:")
	self.lblAscenderVersion = wx.StaticText(self, -1, "\nno version")
	ascenderASizer = wx.BoxSizer(wx.HORIZONTAL)
	ascenderASizer.Add(ascenderVersionHeadline, 0, wx.TOP|wx.RIGHT, 20)

	ascenderBSizer = wx.BoxSizer(wx.HORIZONTAL)
	ascenderBSizer.Add(self.lblAscenderVersion, 0, wx.TOP, 3)
	ascenderSizer = wx.BoxSizer(wx.HORIZONTAL)
	ascenderSizer.Add(ascenderASizer, 0, wx.ALL, 5)
	ascenderSizer.Add(ascenderBSizer, 0, wx.ALL, 5)

        remoteVersionHeadline = wx.StaticText(self, -1, "Remote Version:")
	self.lblRemoteVersion = wx.StaticText(self, -1, "\nno version")
	remoteASizer = wx.BoxSizer(wx.HORIZONTAL)
	remoteASizer.Add(remoteVersionHeadline, 0, wx.TOP|wx.RIGHT, 20)
	remoteBSizer = wx.BoxSizer(wx.HORIZONTAL)
	remoteBSizer.Add(self.lblRemoteVersion, 0, wx.TOP, 0)
	remoteSizer = wx.BoxSizer(wx.HORIZONTAL)
	remoteSizer.Add(remoteASizer, 0, wx.ALL, 5)
	remoteSizer.Add(remoteBSizer, 0, wx.ALL, 10)

        statBoxSizer.Add(ascenderSizer, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 10)
        statBoxSizer.Add(remoteSizer, 0, wx.BOTTOM|wx.LEFT, 10)
        statBoxSizer.Add(txtNull, 0, wx.LEFT, 1000)
        statBoxSizer.Add(txtNull2, 0, wx.BOTTOM, 5)

	return statBoxSizer

    def setup_config_sizer(self):
	statBoxDownload = wx.StaticBox(self, wx.ID_ANY, '  Configuration')
	statBoxDownload.SetBackgroundColour(GREY)
	statBoxDownload.SetForegroundColour(BLACK)
        statBoxSizer = wx.StaticBoxSizer(statBoxDownload, wx.VERTICAL)

        txtNull = wx.StaticText(self, wx.ID_ANY, ' ')

        self.txtConfiguration = wx.StaticText(self, -1, "Configuration file:")
        self.txtFileName = wx.StaticText(self, -1, "No config file selected")

        self.gauge = wx.Gauge(self, range = 23, size = (250, 25)) 

	configSizer = wx.BoxSizer(wx.HORIZONTAL)
        configSizer.Add(self.txtConfiguration, 0, wx.TOP|wx.LEFT, 10)
        configSizer.Add(self.txtFileName, 0, wx.TOP|wx.LEFT, 10)
        configSizer.Add(self.gauge, 0, wx.TOP|wx.LEFT, 10)

        self.btnSaveParam= wx.Button(self, wx.ID_ANY, 'Save Param')
        self.Bind(wx.EVT_BUTTON, self.onSaveParam, self.btnSaveParam)

        statBoxSizer.Add(configSizer, 0, wx.ALL, 15)
        statBoxSizer.Add(self.btnSaveParam, 0, wx.ALL, 15)
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
	self.get_version()

    def onDownload(self, event):
        logging.info('')
	print_const()

    def onCombo(self, event):
        print 'Selected port: '

    def onSaveParam(self, event):
        # add check if param file has been loaded
        logging.info('')

