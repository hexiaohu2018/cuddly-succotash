import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)

        # 创建一个面板
        panel = wx.Panel(self)

        # 创建一个按钮，点击后弹出对话框
        button = wx.Button(panel, label="点击弹出对话框")
        button.Bind(wx.EVT_BUTTON, self.OnButtonClick)

        # 创建一个布局管理器，将按钮添加到面板上
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(button, 0, wx.ALL, 10)
        panel.SetSizer(sizer)

    def OnButtonClick(self, event):
        # 创建一个消息对话框
        dlg = wx.MessageDialog(self, "密码错误！", "错误", wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()

# 创建一个应用程序对象
app = wx.App()

# 创建一个框架窗口
frame = MyFrame(None, title="我的应用程序")
frame.Show()

# 启动应用程序的消息循环
app.MainLoop()
