import wx

GREY  = (180, 180, 180)
BLACK = (0, 0, 0)

class DownLoaderForm(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
	downloadSizer = self.setup_download_sizer()
	connectSizer = self.setup_connect_sizer()

        topSizer = wx.BoxSizer(wx.VERTICAL)
	topSizer.Add(connectSizer, 0, wx.TOP|wx.LEFT, 10)
	topSizer.Add(downloadSizer, 0, wx.TOP|wx.LEFT, 10)
        self.SetSizer(topSizer)

    def setup_connect_sizer(self):
	statBoxDownload = wx.StaticBox(self, wx.ID_ANY, '  Connect')
	statBoxDownload.SetBackgroundColour(GREY)
	statBoxDownload.SetForegroundColour(BLACK)
        statBoxSizer = wx.StaticBoxSizer(statBoxDownload, wx.VERTICAL)

        txtNoConnection = wx.StaticText(self, wx.ID_ANY, 'Not connected')
        btnConnect = wx.Button(self, wx.ID_ANY, 'Connect')
        txtNull = wx.StaticText(self, wx.ID_ANY, ' ')

	connectSizer = wx.BoxSizer(wx.HORIZONTAL)
        connectSizer.Add(btnConnect, 0, wx.BOTTOM|wx.LEFT, 10)
        connectSizer.Add(txtNoConnection, 0, wx.TOP|wx.LEFT, 6)

        statBoxSizer.Add(txtNull, 0, wx.LEFT, 1000)
        statBoxSizer.Add(connectSizer, 0, wx.LEFT, 10)

	return statBoxSizer

    def setup_download_sizer(self):
	statBoxDownload = wx.StaticBox(self, wx.ID_ANY, '  Downloader')
	statBoxDownload.SetBackgroundColour(GREY)
	statBoxDownload.SetForegroundColour(BLACK)
        statBoxSizer = wx.StaticBoxSizer(statBoxDownload, wx.VERTICAL)

        txtNull = wx.StaticText(self, wx.ID_ANY, ' ')

        ascenderVersion = wx.StaticText(self, -1, "Ascender Version:")
        remoteVersion = wx.StaticText(self, -1, "Remote Version:")

        btnDownload = wx.Button(self, wx.ID_ANY, 'Download')
        statBoxSizer.Add(btnDownload, 0, wx.ALL, 20)
        statBoxSizer.Add(ascenderVersion, 0, wx.ALL, 20)
        statBoxSizer.Add(txtNull, 0, wx.LEFT, 1000)
        statBoxSizer.Add(remoteVersion, 0, wx.ALL, 20)

	return statBoxSizer
