#coding:utf-8
import wx
import optparse
import time
import threading
#线程函数
class FuncThread(threading.Thread):
    def __init__(self, func, *params, **paramMap):
        threading.Thread.__init__(self)
        self.func = func
        self.params = params
        self.paramMap = paramMap
        self.rst = None
        self.finished = False

    def run(self):
        self.rst = self.func(*self.params, **self.paramMap)
        self.finished = True

    def getResult(self):
        return self.rst

    def isFinished(self):
        return self.finished

def doInThread(func, *params, **paramMap):
    t_setDaemon = None
    if 't_setDaemon' in paramMap:
        t_setDaemon = paramMap['t_setDaemon']
        del paramMap['t_setDaemon']
    ft = FuncThread(func, *params, **paramMap)
    if t_setDaemon != None:
        ft.setDaemon(t_setDaemon)
    ft.start()
    return ft




class Frame(wx.Frame): #Frame 进行初始化
    def __init__(self,title):
        wx.Frame.__init__(self,None,title=title,size = (900,700))
        boxSizer = wx.BoxSizer(wx.VERTICAL) #初始化一个boxSizer模型

        #初始化一个菜单栏
        menuBar = wx.MenuBar() 
        
        #初始化三个主菜单项
        fileMenu = wx.Menu() 
        waitMenu = wx.Menu()
        helpMenu = wx.Menu()

        #分别为三个主菜单项添加子菜单
        fileMenu.Append(5001,'设置hosts')
        fileMenu.AppendSeparator()
        fileMenu.Append(5005,'清空')
        fileMenu.Append(5009,'E&xit\tAlt+X')

        waitMenu.Append(6001, '卡死')
        waitMenu.Append(6002, '不阻塞')

        helpMenu.Append(7001, '关于')

        #为各自菜单选项绑定事件函数
        self.Bind(wx.EVT_MENU,self.ShowAbout,id = 7001)
        self.Bind(wx.EVT_MENU,self.wait,id=6001)
        self.Bind(wx.EVT_MENU,self.nowait,id=6002)



        #将三个菜单项添加到menuBar中
        menuBar.Append(fileMenu,'文件(&F)')
        menuBar.Append(waitMenu, '卡死(&K)')
        menuBar.Append(helpMenu,'帮助(&H)')

        #将menuBar添加到主Frame中
        self.SetMenuBar(menuBar)

        #初始化一个panel
        self.panel = wx.Panel(self)
        boxSizer.Add(self.panel,3,wx.ALL|wx.EXPAND,3)

        #初始化一个textCtrl,StaticText 需要放到一个panel中，也就是上面创建的那个panel
        self.output = wx.TextCtrl(self.panel,-1,'',style = wx.TE_MULTILINE|wx.HSCROLL, size=(800, 600))

    def ShowAbout(self,evt):#事件函数要传一个evt(事件)为参数
    	wx.MessageDialog(self,'wxPython使用介绍','提示',wx.OK|wx.ICON_INFORMATION).ShowModal()

    def wait(self,evt):
        self.output.AppendText('begin...\r\n')
        time.sleep(10)
        self.output.AppendText('end...\r\n')

    def nowait(self,evt):
        def wait():
            wx.CallAfter(self.output.AppendText,'begin_noblock...\r\n')
            time.sleep(10)
            wx.CallAfter(self.output.AppendText,'end_noblock...\r\n')
        doInThread(wait)



class App(wx.App): ##继承wx,App
    def OnInit(self): ##还没有调起来的时候读取初始化
        self.frame = Frame('修改host工具')        
        self.frame.Centre()
        self.frame.Show(True)        
        return True

def killSelf(evt = None):
    os.system('taskkill /F /T /PID %d >NUL 2>NUL' % win32process.GetCurrentProcessId())

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-x', '--no-update', dest = 'test', action = 'store_true', help = 'start without update')
    parser.add_option('-t', '--no-update-test', dest = 'test2', action = 'store_true', help = 'start without update debug')
    options, args = parser.parse_args()
    if options.test:
        print("-x param")
    if options.test2:
        print("-t param")
    App(redirect = False).MainLoop()