import time
import wx


from threading import Thread

from wx.lib.pubsub import pub

class TestThread(Thread):

    def __init__(self):

        Thread.__init__(self)
        self.start()

    def run(self):

        for i in range(10):
            time.sleep(1)
            wx.CallAfter(pub.sendMessage,"update",msg="")

class MyProgressDialog(wx.Dialog):

    def __init__(self):

        wx.Dialog.__init__(self,None,title ="Download_Bar")
        self.count = 0

        self.progress = wx.Gauge(self,range = 20)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.progress,0,wx.EXPAND)
        self.SetSizer(sizer)

        pub.subscribe(self.updateProgress, "update")

    def updateProgress(self, msg):
        
        self.count += 1
        if self.count >= 20:
            self.Destroy()
        self.progress.SetValue(self.count)


class MyForm(wx.Frame):
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Tutorial")
        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
        self.btn = btn = wx.Button(panel, label="Start Thread")
        btn.Bind(wx.EVT_BUTTON, self.onButton)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
        panel.SetSizer(sizer)
    #----------------------------------------------------------------------
    def onButton(self, event):
    
        btn = event.GetEventObject()
        btn.Disable()
        TestThread()
        dlg = MyProgressDialog()
        dlg.ShowModal()
        btn.Enable()
#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm().Show()
    app.MainLoop()