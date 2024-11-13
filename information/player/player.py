import pygame
import os
import wx


class PlayMusic:

    def __init__(self):
        pygame.mixer.init()
        self.isPause = False  #用于判断有没有暂停

    def play(self):
        self.pos = 0  #用于记录当前音频位置，实现快进快退
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():  #检查是否正在播放，若正在播放则等待播放完毕
            pygame.time.Clock.tick(10)

    def pause(self):
        if self.isPause:  #检查当前播放状态是不是暂停，若是则继续播放
            pygame.mixer.music.unpause()
            self.isPause = False
        else:  #如果正在播放就暂停
            pygame.mixer.music.pause()
            self.isPause = True

    def loadFile(self, musicPath):
        pygame.mixer.music.load(musicPath)

    def right(self):
        self.pos += 5
        pygame.mixer.music.set_pos(self.pos)

    def left(self):
        self.pos = max(0, self.pos - 5)
        pygame.mixer.music.set_pos(self.pos)


class MyFrame(wx.Frame):

    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)
        self.__initUI()
        self.playmusic = PlayMusic()
        self.__initEVT()

    def __initUI(self):
        self.SetTitle('播放器')
        self.menubar = wx.MenuBar()
        self.media = wx.Menu()
        self.play = wx.Menu()

        panel = wx.Panel(self)
        wx.StaticText(panel, label='音乐')
        self.musicList = wx.ListBox(panel)

        self.openMusicMenu = self.media.Append(wx.ID_ANY, '打开音乐(&o)')
        self.exitMenu = self.media.Append(wx.ID_ANY, '退出(&x)')

        self.playMenu = self.play.Append(wx.ID_ANY, '播放(&p)')
        self.PauseMenu = self.play.Append(wx.ID_ANY, '暂停(&t)')
        self.rightMenu = self.play.Append(wx.ID_ANY, '快进(&r)')
        self.leftMenu = self.play.Append(wx.ID_ANY, '快退(&L)')

        self.menubar.Append(self.media, '媒体(&M)')
        self.menubar.Append(self.play, '播放(&P)')
        self.SetMenuBar(self.menubar)

    def __initEVT(self):

        #绑定菜单事件
        self.Bind(wx.EVT_MENU, self.OnOpenMusicFile, self.openMusicMenu)
        self.Bind(wx.EVT_MENU, self.OnExit, self.exitMenu)

        self.Bind(wx.EVT_MENU, self.OnPlay, self.playMenu)
        self.Bind(wx.EVT_MENU, self.OnPause, self.PauseMenu)
        self.Bind(wx.EVT_MENU, self.OnRight, self.rightMenu)
        self.Bind(wx.EVT_MENU, self.OnLeft, self.leftMenu)

        #绑定快捷键
        self.musicList.Bind(wx.EVT_CHAR_HOOK, self.OnKeyDown)
        shortcuts = wx.AcceleratorTable([
            (wx.ACCEL_CTRL, ord('O'), self.openMusicMenu.GetId()),  #打开音乐
        ])
        self.SetAcceleratorTable(shortcuts)

    def OnExit(self):
        self.Close()

    def OnPlay(self, e):

        #设置当前播放的音乐为窗口标题
        title = self.setPath()
        self.playmusic.loadFile(title)
        title = title.rstrip('.mp3')
        self.SetTitle(os.path.basename(title) + '\n播放器')

        self.playmusic.play()

    def OnKeyDown(self, e: wx.KeyEvent):
        key = e.GetKeyCode()

        if key == wx.WXK_RETURN:  #当按下回车键播放列表当前选定的文件
            self.playmusic.loadFile(self.setPath())
            self.OnPlay(None)
        elif key == wx.WXK_RIGHT:  #当按下右光标快进
            self.OnRight(None)
        elif key == wx.WXK_LEFT:  #按下左光彪快退
            self.OnLeft(None)
        elif key == wx.WXK_SPACE:  #按下空格键暂停继续
            self.OnPause(None)
        else:
            e.Skip()

    def setPath(self):
        index = self.musicList.GetSelection()
        path = self.musicList.GetClientData(index)
        return path

    def OnPause(self, e):
        self.playmusic.pause()

    def OnRight(self, e):
        self.playmusic.right()

    def OnLeft(self, e):
        self.playmusic.left()

    def OnOpenMusicFile(self, e):
        wildcard = '.mp3音频文件|*.mp3'
        fileName = wx.FileDialog(self,
                                 '打开音乐',
                                 wildcard=wildcard,
                                 style=wx.FD_FILE_MUST_EXIST
                                 | wx.FD_DEFAULT_STYLE)

        if fileName.ShowModal() == wx.ID_OK:
            path = fileName.GetPath()
            self.musicList.Append(os.path.basename(path))
            self.musicList.SetClientData(self.musicList.GetCount() - 1, path)
            self.musicList.SetSelection(self.musicList.GetCount() -
                                        1)  #设置列表索引到最后一个项目
            fileName.Destroy()


app = wx.App()
p = MyFrame(None)
p.Show()
app.MainLoop()
