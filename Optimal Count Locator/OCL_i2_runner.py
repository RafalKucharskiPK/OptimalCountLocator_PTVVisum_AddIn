import time
import OCL_i2 as OCL
import wx



class OCL_GUI(OCL.MyFrame):
    def __init__(self,Visum):
        OCL.MyFrame.__init__(self,Visum)

try:
    Visum
    standalone=False
except:
    import win32com.client
    Visum=win32com.client.Dispatch("Visum.Visum.13")
    Visum.LoadVersion("E:/Krakow.ver")
    #Visum.LoadVersion("D:/B.ver")
    
    standalone=True


if __name__ == "__main__":
    if standalone:
        app = wx.PySimpleApp(0)    
    wx.InitAllImageHandlers()
    GUI_OCL = OCL_GUI(Visum)
    app.SetTopWindow(GUI_OCL)
    GUI_OCL.Show()
    if standalone:
        app.MainLoop()