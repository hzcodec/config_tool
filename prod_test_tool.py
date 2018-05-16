#i!/usr/bin/python

# Auther      : Heinz Samuelsson
# Date        : 2017-06-02
# File        : prod_test_tool.py
# Reference   : -
# Description : Production test tool for ActSafe.
#               
# Python ver  : 2.7.3 (gcc 4.6.3)

import wx
import downloader
import calibration
import prodtest
import trace
import logview
import logging
from wx.lib.pubsub import pub
from wx.lib.pubsub import setupkwargs

WINDOW_SIZE = (1035, 870)

HEADLINE = 70*' '+'Production Test Tool, ACX/TCX'

# color codes
GREY  = (180, 180, 180)
BLACK = (0, 0, 0)

# setup logging function
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s : %(funcName)s() - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def print_const():
   app = wx.GetApp()
   #print app.frame.tabDownLoader.ser


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

	self.exitDialog =  wx.MessageDialog( self, "Quit application?\n\nCheck that Ascender motor has stopped!\n", "Quit", wx.YES_NO)

	self.Centre()
 
        # create a panel and notebook (tabs holder)
        p = wx.Panel(self)
        nb = wx.Notebook(p)
 
        # Create the tab windows
        self.tabDownLoader = downloader.DownLoaderForm(nb)
        tabCalib = calibration.CalibForm(nb)
        self.tabProdTest = prodtest.ProdTestForm(nb)
        tabTrace = trace.TraceTestForm(nb)
        #tabLogView = logview.LogViewForm(nb)

        # add the windows to tabs and name them
        nb.AddPage(self.tabDownLoader, "Common")
        nb.AddPage(tabCalib, "Calibrate")
        nb.AddPage(self.tabProdTest, "Prod Test")
        nb.AddPage(tabTrace, "Performance Test")
        #nb.AddPage(tabLogView, "Log")

        self.setup_menu()

        # set noteboook in a sizer to create the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

    def setup_menu(self):
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        unlockMenu = wx.Menu()
        aboutMenu = wx.Menu()

	fileMenu.Append(wx.ID_OPEN, "Open", "Open")
	fileMenu.Append(wx.ID_SAVE, "Save", "Save")
	fileMenu.Append(wx.ID_EXIT, "Exit", "Close")
	unlockMenu.Append(101, "&Lock\tCTRL+L", "Lock")
	unlockMenu.Append(102, "&UnLock\tCTRL+U", "UnLock")
	aboutMenu.Append(103, "&About\tCTRL+A", "Open")

	# disable 'Save' menu
	fileMenu.Enable(wx.ID_SAVE, False)

	menuBar.Append(fileMenu, "&File")
	menuBar.Append(unlockMenu, "&Enable Params")
	menuBar.Append(aboutMenu, "&About")
	self.SetMenuBar(menuBar)
	self.Bind(wx.EVT_MENU, self.onOpen, id=wx.ID_OPEN)
	self.Bind(wx.EVT_MENU, self.onSave, id=wx.ID_SAVE)
	self.Bind(wx.EVT_MENU, self.onQuit, id=wx.ID_EXIT)
	self.Bind(wx.EVT_MENU, self.onLock, id=101)
	self.Bind(wx.EVT_MENU, self.onUnLock, id=102)
	self.Bind(wx.EVT_MENU, self.onAbout, id=103)

    def onOpen(self, event):
        print_const()
	openFileDialog = wx.FileDialog(self, "Open", "", "", "ACX/TCX config files (*.txt)|*.txt", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        openFileDialog.GetPath()
	#print openFileDialog.GetPath()

	with open(openFileDialog.GetPath()) as f:
          lines = f.readlines()

        # pass configuration parameters to downloader and prodtest
	pub.sendMessage('configListener', message=lines, fname=openFileDialog.GetFilename())
	self.tabDownLoader.print_parameters()
        openFileDialog.Destroy()

    def onSave(self, event):
	saveFileDialog = wx.FileDialog(self, "Save As", "", "", "ACX/TCX config files (*.txt)|*.txt", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        saveFileDialog.ShowModal()
        saveFileDialog.GetPath()

        print '--->', self.tabProdTest.configParameters

        saveFileDialog.Destroy()

    def onLock(self, event):
        self.tabProdTest.lock_text_controls()

    def onQuit(self, event):
        rv = self.exitDialog.ShowModal()

        if rv == wx.ID_YES:
            self.Close(True)

    def onUnLock(self, event):
        dialog = wx.TextEntryDialog(self, message="Enter Password", caption="Password query", style=wx.OK|wx.CANCEL|wx.TE_PASSWORD)
        dialog.SetValue("")
        result = dialog.ShowModal()

        # check password if OK button was pressed
        if result == wx.ID_OK:
            passwd = dialog.GetValue()

            if (passwd == 'Woodpecker'):

                self.tabProdTest.txtCtrl_cl_max.Enable()
                self.tabProdTest.txtCtrl_cl_min.Enable()
                self.tabProdTest.txtCtrl_sl_ki.Enable()
                self.tabProdTest.txtCtrl_sl_kp.Enable()
                self.tabProdTest.txtCtrl_sl_max.Enable()
                self.tabProdTest.txtCtrl_sl_min.Enable()
                self.tabProdTest.txtCtrl_has_switch.Enable()
                self.tabProdTest.txtCtrl_power_margin.Enable()
                self.tabProdTest.txtCtrl_power_factor.Enable()
                self.tabProdTest.txtCtrl_brightness_lo.Enable()
                self.tabProdTest.txtCtrl_brake_temp_ok.Enable()
                self.tabProdTest.txtCtrl_brake_temp_hi.Enable()
                self.tabProdTest.txtCtrl_brake_max_id.Enable()
                self.tabProdTest.txtCtrl_brake_pos_ratio.Enable()
                self.tabProdTest.txtCtrl_trajec_acc.Enable()
                self.tabProdTest.txtCtrl_trajec_ret.Enable()
                self.tabProdTest.txtCtrl_dominant_throttle_on.Enable()
                self.tabProdTest.txtCtrl_max_motor_temp.Enable()
                self.tabProdTest.txtCtrl_num_motor_ch.Enable()
                self.tabProdTest.txtCtrl_idle_timeout.Enable()
                self.tabProdTest.txtCtrl_rope_stuck_on.Enable()
                self.tabProdTest.txtCtrl_iq_alpha.Enable()
                self.tabProdTest.txtCtrl_speed_alpha.Enable()
                self.tabProdTest.txtCtrl_undershoot.Enable()
                self.tabProdTest.txtCtrl_speed_lim.Enable()
                self.tabProdTest.txtCtrl_delay_start.Enable()

    def onAbout(self, event):
        licence = """

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR 
OTHER DEALINGS IN THIS SOFTWARE.
         """
        description = """Version PA2.

    """

        info = wx.AboutDialogInfo()
        info.SetName("Production Test Tool for ActSafe's ACX/TCX")
        info.SetDescription(description)
        info.SetCopyright('(C) 2017 - Unjo AB')
        info.SetWebSite('http://www.unjo.com')
        info.SetLicence(licence)
        wx.AboutBox(info)


class mainApp(wx.App):
   def OnInit(self):
       self.frame = MainFrame(None, -1, title=HEADLINE, style=wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX, size=WINDOW_SIZE)
       self.frame.Show()
       return True

if __name__ == '__main__':
    app = mainApp() 
    app.MainLoop()
