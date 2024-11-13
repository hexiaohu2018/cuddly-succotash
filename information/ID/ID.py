import wx
import re

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)
        panel = wx.Panel(self)
        self.label = wx.StaticText(panel, label="请输入身份证号", pos=(10, 10))
        self.text_ctrl = wx.TextCtrl(panel, pos=(10, 30))
        self.button = wx.Button(panel, label="查询", pos=(10, 60))
        self.button.Bind(wx.EVT_BUTTON, self.on_button_click)
        self.SetSize((300, 200))
        self.SetTitle("身份证出生日期提取")

    def on_button_click(self, event):
        id_number = self.text_ctrl.GetValue()
        if self.is_valid_id(id_number):
            birth_date = self.extract_birth_date(id_number)
            wx.MessageBox(f"出生日期: {birth_date}", "查询结果", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("无效的身份证号码", "错误", wx.OK | wx.ICON_ERROR)

    def is_valid_id(self, id_number):
        pattern = r'^\d{17}[\dXx]$'
        return re.match(pattern, id_number) is not None

    def extract_birth_date(self, id_number):
        birth_date_str = id_number[6:14]
        year = birth_date_str[:4]
        month = birth_date_str[4:6]
        day = birth_date_str[6:8]
        return f"{year}年{month}月{day}日"

if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame(None)
    frame.Show(True)
    app.MainLoop()