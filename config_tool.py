#!/usr/bin/python
# https://www.blog.pythonlibrary.org/2010/05/22/wxpython-and-threads/
# https://www.blog.pythonlibrary.org/2008/06/11/wxpython-creating-an-about-box/

# Print a list of available ports
#   > python -m serial.tools.list_ports

# Console based terminal
#   > python -m serial.tools.miniterm /dev/ttyACM0

# Create one binary file
#   > pyinstaller --onefile config.py 

import wx
import serial
import time
import platform
import glob
import sys
import datetime
import threading
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub as Publisher

# button start position
Xpos  = 10
Ypos  = 250
Ypos2 = 80

WINDOW_SIZE = (800, 600)
ALIGN_MSG   = (Xpos+120, Ypos+7)
CALIB_MSG1  = (Xpos+120, Ypos+67)
CALIB_MSG2  = (Xpos+120, Ypos+107)
CALIB_MSG3  = (Xpos+120, Ypos+147)
RED         = (255, 0, 0)
GREEN       = (36, 119, 62)
BLUE        = (0, 0, 255)

btnClosePos        = (Xpos+650, Ypos+290)
btnSavePos         = (Xpos, Ypos+290)
btnConnectPos      = (Xpos+250, 26)
btnAlignPos        = (Xpos, Ypos)
btnCalibRightPos   = (Xpos, Ypos+60)
btnCalibLeftPos    = (Xpos, Ypos+100)
btnCalibNormalPos  = (Xpos, Ypos+140)
btnCalibRestartPos = (Xpos, Ypos+180)

DELIMITER = 190*'.'


def list_serial_ports():
    system_name = platform.system()
    print system_name

    if system_name == "Windows":
        # Scan for available ports.
        available = []

        for i in range(256):
            try:
                s = serial.Serial(i)
                available.append(i)
                s.close()
            except serial.SerialException:
                pass
        return available

    elif system_name == "Darwin":
        # Mac
        return glob.glob('/dev/tty*') + glob.glob('/dev/cu*')

    else:
        # Assume Linux or something else
        return glob.glob('/dev/ttyA*') + glob.glob('/dev/ttyUSB*')


def serial_cmd(cmd, serial):
    # send command to serial port
    serial.write(cmd+'\r');
    serial.reset_input_buffer()
    serial.reset_output_buffer()
    serial.flush()

    # read data from serial port
    c = serial.read(1300)
    return c


class PollAlignment(threading.Thread):

    def __init__(self, serial):
        threading.Thread.__init__(self)
	self.ser = serial
        self.start()    # start the thread
 
    def run(self):
        time.sleep(1)
	line = []

        while True:
            for c in self.ser.read():
                line.append(c)
                if (c == '\n'):
		    s = [''.join(line[:])]
		    t = s[0]
                    print t[:-2]
                    line = []
                    wx.CallAfter(Publisher.sendMessage, "topic_aligned", "Aligned done")
                    break


class MyForm(wx.Frame):
 
    def __init__(self):
	# not sizeable window
        wx.Frame.__init__(self, None, wx.ID_ANY, "Built in Test Tool for ACX/TCX", size=WINDOW_SIZE, style=wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX)
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.panel.SetBackgroundColour((240, 220, 210))
	self.CenterOnScreen()
        #self.panel.SetBackgroundColour((212, 170, 103))

        img1 = wx.Image('logo.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
	img2 = wx.ImageFromBitmap(img1)
        width = 80 
        height = 40
	img3 = img2.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
	result = wx.BitmapFromImage(img3)
        wx.StaticBitmap(self.panel, -1, result, (680, 15))

	self.menuBar = wx.MenuBar()
	self.fileMenu = wx.Menu()

	self.menuBar.Append(self.fileMenu, "Config")
	aboutMenuItem = self.fileMenu.Append(wx.ID_ABOUT, "About", "Information about the application")
	exitMenuItem = self.fileMenu.Append(wx.NewId(), "Exit", "Exit the application")
	self.Bind(wx.EVT_MENU, self.onClose, exitMenuItem)
	self.Bind(wx.EVT_MENU, self.onAbout, aboutMenuItem)
        self.SetMenuBar(self.menuBar)

        self.defineButtons()
	self.defineCombo()

	self.lblConnected = wx.StaticText(self.panel, label= '-----', pos=(390,35))
	self.lblConfigSaved = wx.StaticText(self.panel, label= '-----', pos=(Xpos+160,Ypos2+466))

        self.lblDelimiter1 = wx.StaticText(self.panel, -1, DELIMITER, pos = (10,60))
        self.lblDelimiter1.SetForegroundColour(wx.Colour(0,0,255))

        self.lblDelimiter2 = wx.StaticText(self.panel, -1, DELIMITER, pos = (10,210))
        self.lblDelimiter2.SetForegroundColour(wx.Colour(0,0,255))

        self.lblDelimiter2 = wx.StaticText(self.panel, -1, DELIMITER, pos = (10,500))
        self.lblDelimiter2.SetForegroundColour(wx.Colour(0,0,255))

	font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
	lblAscendVer = wx.StaticText(self.panel, label='Ascender version:', pos=(Xpos+5,Ypos2+17))
	lblAscendVer.SetFont(font)
	lblRemoteVer = wx.StaticText(self.panel, label='Remote version:', pos=(Xpos+5,Ypos2+77))
	lblRemoteVer.SetFont(font)

	self.lblAlign = wx.StaticText(self.panel, label='Alignment not done!', pos=ALIGN_MSG)
	self.lblCalibRight = wx.StaticText(self.panel, label='Turn throttle handle max Up', pos=CALIB_MSG1)
	self.lblCalibLeft = wx.StaticText(self.panel, label='Turn throttle handle max Down', pos=CALIB_MSG2)
	self.lblCalibNormal = wx.StaticText(self.panel, label='Set throttle handle in neutral position', pos=CALIB_MSG3)

	self.printPortName()

    def defineButtons(self):
        self.btnClose = wx.Button(self.panel, label="Close",  pos=btnClosePos, size=(110, 30))
        self.btnSaveConfig = wx.Button(self.panel, label="Save Configuration",  pos=btnSavePos, size=(150, 30))
        self.btnConnect = wx.Button(self.panel, label="Connect",  pos=btnConnectPos, size=(110, 30))
        self.btnAlign = wx.Button(self.panel, label="Align",  pos=btnAlignPos, size=(110, 30))

        self.btnCalibRight = wx.Button(self.panel, id=wx.ID_ANY, label="Calib Right", name="calibr", pos=btnCalibRightPos, size=(110, 30))
        self.btnCalibLeft = wx.Button(self.panel, id=wx.ID_ANY, label="Calib Left", name="calibl", pos=btnCalibLeftPos, size=(110, 30))
        self.btnCalibNormal = wx.Button(self.panel, id=wx.ID_ANY, label="Calib Neutral", name="calibn", pos=btnCalibNormalPos, size=(110, 30))
        self.btnCalibRestart = wx.Button(self.panel, id=wx.ID_ANY, label="Calib Restart", name="calibr", pos=btnCalibRestartPos, size=(110, 30))
	self.btnCalibLeft.Enable(False)
	self.btnCalibNormal.Enable(False)

	self.bindButtons()

	Publisher.subscribe(self.aligned_finished, "topic_aligned")
	 

    def bindButtons(self):
	self.Bind(wx.EVT_BUTTON, self.onClose, id=self.btnClose.GetId())
	self.Bind(wx.EVT_BUTTON, self.onSaveConfiguration, id=self.btnSaveConfig.GetId())
	self.Bind(wx.EVT_BUTTON, self.onConnect, id=self.btnConnect.GetId())
	self.Bind(wx.EVT_BUTTON, self.onAlign, id=self.btnAlign.GetId())
	self.Bind(wx.EVT_BUTTON, self.onCalibRight, id=self.btnCalibRight.GetId())
	self.Bind(wx.EVT_BUTTON, self.onCalibLeft, id=self.btnCalibLeft.GetId())
	self.Bind(wx.EVT_BUTTON, self.onCalibNormal, id=self.btnCalibNormal.GetId())
	self.Bind(wx.EVT_BUTTON, self.onCalibRestart, id=self.btnCalibRestart.GetId())
    

    def defineCombo(self):
        portNames = ['ACM0', 'ACM1', 'USB0']
        self.combo = wx.ComboBox(self.panel, choices=portNames, pos=(140, 27))
        self.combo.SetSelection(0) # preselect ACM0
        self.combo.Bind(wx.EVT_COMBOBOX, self.onCombo)
    

    def printPortName(self):
	font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
	lblHead1 = wx.StaticText(self.panel, label='Serial Port:', pos=(Xpos+5,35))
	lblHead1.SetFont(font)

        #ports = list_serial_ports()
	#port2 = "".join(ports)
	#port3 = port2[5:]
	#font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
	#lblHead1 = wx.StaticText(self.panel, label=port3, pos=(Xpos+140,Ypos2-15))
	#lblHead1.SetFont(font)

    
    def getVersion(self):
        ver = serial_cmd('v', self.ser)
	lblAscenderVersion = wx.StaticText(self.panel, label= ver[1:], pos=(150,Ypos2))
 
        ver = serial_cmd('r_v', self.ser)
	lblRemoteVersion = wx.StaticText(self.panel, label= ver[3:], pos=(150,Ypos2+60))
    

    def onClose(self, event):
        self.Close()

    def onAbout(self, event):
        info = wx.AboutDialogInfo()
        info.Name = "Configuration Tool"
        info.Version = "0.1 Beta"
	info.Description = "The tool is used to configure Actsafe's Ascender ACX/TCX"
        info.Developers = ["Heinz Samuelsson, Unjo AB"]
        wx.AboutBox(info)


    def onSaveConfiguration(self, event):
	now = datetime.datetime.now().strftime("%Y-%m-%d   %H:%M")
	self.lblConfigSaved.SetLabel('Configuration saved at: ' + str(now))


    def onConnect(self, event):
	try:
            self.ser = serial.Serial(port = '/dev/tty'+self.combo.GetValue(),
                                     baudrate = 9600,
                                     parity = serial.PARITY_NONE,
                                     stopbits = serial.STOPBITS_ONE,
                                     bytesize = serial.EIGHTBITS,
                                     timeout = 1)

            self.getVersion()
	    self.lblConnected.SetLabel(self.combo.GetValue() + ' connected')
            self.lblConnected.SetForegroundColour(wx.Colour(0,0,255))

	except:
	    self.lblConnected.SetLabel('Cannot connect ' + self.combo.GetValue())
            self.lblConnected.SetForegroundColour(wx.Colour(255,0,0))
	    print 'Error, could not open port ' + self.combo.GetValue()


    def onAlign(self, event):
	PollAlignment(self.ser)
        ver = serial_cmd('align', self.ser)
	print ver

	self.lblAlign.SetForegroundColour(BLUE)
	self.lblAlign.SetLabel("Alignment initiated")
	self.lblConfigSaved.SetLabel(' ')
	self.btnAlign.Enable(False)
	self.btnCalibRight.Enable(False)
	self.btnCalibRestart.Enable(False)


    def onCalibRight(self, event):
        print 'Calib right'
	self.btnCalibRight.Enable(False)
	self.btnCalibLeft.Enable(True)
	self.lblAlign.SetForegroundColour(GREEN)
	self.lblCalibRight.SetLabel("Up Calibration finished")


    def onCalibLeft(self, event):
        print 'Calib left'
	self.btnCalibLeft.Enable(False)
	self.btnCalibNormal.Enable(True)
	self.lblCalibLeft.SetLabel("Down Calibration finished")


    def onCalibNormal(self, event):
        print 'Calib normal'
	self.btnCalibNormal.Enable(False)
	self.lblCalibNormal.SetLabel("Neutral Calibration finished")


    def onCalibRestart(self, event):
	self.btnCalibRight.Enable(True)
	self.lblConfigSaved.SetLabel(' ')
	self.lblCalibRight.SetLabel("Turn throttle handle max Up")
	self.lblCalibLeft.SetLabel("Turn throttle handle max Down")
	self.lblCalibNormal.SetLabel("Set throttle handle in neutral position")


    def onCombo(self, event):
        print 'Selected port: ' + self.combo.GetValue()
	#self.label.SetLabel("selected "+ self.combo.GetValue() +" from Combobox") 
        #print('Connected to: ' + self.ser.portstr)

    def aligned_finished(self, msg):

        t = msg.data

	if isinstance(t, int):
	    print 't:', t
	else:
	    print 'else', t
	    self.btnAlign.Enable(True)
	    self.lblAlign.SetForegroundColour(GREEN)
	    self.lblAlign.SetLabel("Alignment finished.")
	    self.btnCalibRight.Enable(True)
	    self.btnCalibRestart.Enable(True)


if __name__ == "__main__":

    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()

