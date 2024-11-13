import wx
from playsound import playsound
import os
import time

def bfyx(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    audio_file_path = os.path.join(script_dir, "sound", file_name)
    playsound(audio_file_path)

def sj(event):
    while True:
        minute = int(time.strftime("%M"))
        if minute == 47:
            bfyx("3.wav")
        else:
            bfyx("2.wav")
        time.sleep(30)

if __name__ == "__main__":
    app = wx.App()
    frm = wx.Frame(None, title='与时排麦提醒')
    pan = wx.Panel(frm)

    button1 = wx.Button(pan, -1, '开始倒计时')
    button1.Bind(wx.EVT_BUTTON, sj)

    frm.Show()
    app.MainLoop()