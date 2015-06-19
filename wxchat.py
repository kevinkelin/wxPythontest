#coding:gbk
import wx
import optparse
import time
import threading
import json,pythoncom
import autonet,urllib

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
        pythoncom.CoInitialize()
        self.rst = self.func(*self.params, **self.paramMap)
        self.finished = True
        pythoncom.CoUninitialize()

    def getResult(self):
        return self.rst

    def isFinished(self):
        return self.finished

def doInThread(func, *params, **paramMap):
    ft = FuncThread(func, *params, **paramMap)
    ft.start()
    return ft

class login(wx.Dialog):
    def __init__(self,parent):
        wx.Dialog.__init__(self,parent,title='登录系统',size = (300,200))
        #初始化一个空行
        self.blackrow = wx.StaticText(self,-1,"")

        #初始化两个文本框
        self.useridtext = wx.StaticText(self,-1,"用户ID")
        self.passtext = wx.StaticText(self,-1,"密码")
        self.userid = wx.TextCtrl(self,-1,'',style=wx.TE_LEFT)
        self.password = wx.TextCtrl(self,-1,'',style=wx.TE_PASSWORD)

        #初始化一个状态显示文本框
        self.info = wx.StaticText(self,-1,'')
        
        #初始化三个按钮
        self.loginBtn = wx.Button(self,-1,"登录")
        self.Bind(wx.EVT_BUTTON,self.loginuser,self.loginBtn)
        self.regBtn = wx.Button(self,-1,"注册")
        self.cancelBtn = wx.Button(self,-1,"退出")

        #初始化一个主窗口
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        useridSizer = wx.BoxSizer(wx.HORIZONTAL)        
        useridSizer.Add(self.useridtext,1)
        useridSizer.Add(self.userid,2)

        passSizer = wx.BoxSizer(wx.HORIZONTAL)
        passSizer.Add(self.passtext,1)
        passSizer.Add(self.password,2)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(self.loginBtn)
        btnSizer.Add(self.regBtn)
        btnSizer.Add(self.cancelBtn)

        mainSizer.Add((-1,20))
        mainSizer.Add(useridSizer,2)
        mainSizer.Add(passSizer,2)
        mainSizer.Add(self.info)
        mainSizer.Add(btnSizer,1)

        self.SetSizer(mainSizer)

        

    def loginuser(self,evt):
        userid = self.userid.GetValue()
        userpass = self.password.GetValue()
        self.info.SetLabel(u'正在以'+userid+u'的身份登录...')
        body=urllib.urlencode({'userId':userid,'pswd':userpass})
        rst = doInThread(autonet.doHttpPost,uri=r"http://pub.releaseoa.corp.qihoo.net:8385/login",body=body)
        while True:
            if not rst.isFinished():
                time.sleep(0.5)
            else:
                print '11111111'
                print rst.getResult()
                break

        
            # status,headers,contents = autonet.doHttpPost(uri=r"http://pub.releaseoa.corp.qihoo.net:8385/login",body=body)
            # print contents




class Frame(wx.Frame): #Frame 进行初始化
    def __init__(self,title):
        wx.Frame.__init__(self,None,title=title,size = (300,600))       

        #初始化一个菜单栏
        menuBar = wx.MenuBar() 
        
        #初始化三个主菜单项
        loginMenu = wx.Menu() 
        talkMenu = wx.Menu()
        helpMenu = wx.Menu()

        #分别为三个主菜单项添加子菜单
        loginMenu.Append(5001,'登录')
        loginMenu.AppendSeparator()
        loginMenu.Append(5005,'登出')
        loginMenu.Append(5009,'E&xit\tAlt+X')

        talkMenu.Append(6001, '检查留言')        

        helpMenu.Append(7001, '关于')

        #给相应的按钮添加方法
        self.Bind(wx.EVT_MENU,self.startLogin,id=5001)

        #将菜单添加到menuBar中
        menuBar.Append(loginMenu,"登录")
        menuBar.Append(talkMenu,"留言")
        menuBar.Append(helpMenu,"关于")

        #将menuBar设置到menu上
        self.SetMenuBar(menuBar)

        #在主恩赐初始化一个盒模型
        boxSizer = wx.BoxSizer(wx.VERTICAL)
        #在主界面初始化一个panel
        self.panel = wx.Panel(self)
        #在panel上添加一个textCtrl
        self.infobox = wx.TextCtrl(self.panel,-1,'qqqq',style = wx.TE_MULTILINE|wx.HSCROLL,size=(300,550))
        boxSizer.Add(self.panel,3,wx.ALL | wx.EXPAND, 3)

    def startLogin(self,evt):
        self.infobox.WriteText('start login...')
        logDig = login(self)
        logDig.Show()

  
class App(wx.App): ##继承wx.App
    def OnInit(self): ##还没有调起来的时候读取初始化
        self.frame = Frame('QA内部IM工具')        
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