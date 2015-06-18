#coding:utf-8
import wx
import optparse

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



        #将三个菜单项添加到menuBar中
        menuBar.Append(fileMenu,'文件(&F)')
        menuBar.Append(waitMenu, '卡死(&K)')
        menuBar.Append(helpMenu,'帮助(&H)')

        #将menuBar添加到主Frame中
        self.SetMenuBar(menuBar)

        #初始化一个panel
        self.panel = wx.Panel(self)
        boxSizer.Add(self.panel,3,wx.ALL|wx.EXPAND,3)

    def ShowAbout(self,evt):#事件函数要传一个evt(事件)为参数
    	wx.MessageDialog(self,'wxPython使用介绍','提示',wx.OK|wx.ICON_INFORMATION).ShowModal()

        


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