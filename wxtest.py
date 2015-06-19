#coding:utf-8
import wx
import optparse
import time
import threading
#�̺߳���
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




class Frame(wx.Frame): #Frame ���г�ʼ��
    def __init__(self,title):
        wx.Frame.__init__(self,None,title=title,size = (900,700))       

        #��ʼ��һ���˵���
        menuBar = wx.MenuBar() 
        
        #��ʼ���������˵���
        fileMenu = wx.Menu() 
        waitMenu = wx.Menu()
        helpMenu = wx.Menu()

        #�ֱ�Ϊ�������˵�������Ӳ˵�
        fileMenu.Append(5001,'����hosts')
        fileMenu.AppendSeparator()
        fileMenu.Append(5005,'���')
        fileMenu.Append(5009,'E&xit\tAlt+X')

        waitMenu.Append(6001, '����')
        waitMenu.Append(6002, '������')

        helpMenu.Append(7001, '����')

        #Ϊ���Բ˵�ѡ����¼�����
        self.Bind(wx.EVT_MENU,self.ShowAbout,id = 7001)
        self.Bind(wx.EVT_MENU,self.wait,id=6001)
        self.Bind(wx.EVT_MENU,self.nowait,id=6002)



        #�������˵�����ӵ�menuBar��
        menuBar.Append(fileMenu,'�ļ�(&F)')
        menuBar.Append(waitMenu, '����(&K)')
        menuBar.Append(helpMenu,'����(&H)')

        #��menuBar��ӵ���Frame��
        self.SetMenuBar(menuBar)

        boxSizer = wx.BoxSizer(wx.VERTICAL) #��ʼ��һ��boxSizerģ��
        #��ʼ��һ��panel
        self.panel = wx.Panel(self)
        boxSizer.Add(self.panel,3,wx.ALL|wx.EXPAND,3) #ǰ���3��ʾ��ͬ��Ԫ�ص���ռ�ȣ������3��border��

        #��ʼ��һ��textCtrl,StaticText ��Ҫ�ŵ�һ��panel�У�Ҳ�������洴�����Ǹ�panel
        #��ʼ�������ʱ��Ҫ���������һ��ID��������ID�Ļ�����ʹ��-1�����һ�Ҫ����һ�����࣬û�п���ʹ��None
        #��Щ�������Ҫ�и������
        self.output = wx.TextCtrl(self.panel,-1,'',style = wx.TE_MULTILINE|wx.HSCROLL, size=(800, 600))
        
        #��ʼ������button��ʵ����һ�����棬һ���ǹر� 
        self.saveBtn = wx.Button(self,-1,'����') 
        
        self.cancelBtn = wx.Button(self, wx.ID_CANCEL, '�ر�')
        canelBtn2 = wx.Button(self,-1,'�ر�2') 
        self.Bind(wx.EVT_BUTTON,self.onClose,id = wx.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON,self.onClose,canelBtn2)
        #�ײ���ʼ��һ����btnSizer��Ȼ��������ť�ŵ����sizer��
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)        
        btnSizer.Add(self.saveBtn,0,wx.ALIGN_CENTER_VERTICAL)
        btnSizer.Add(self.cancelBtn,0,wx.ALIGN_CENTER_VERTICAL)
        btnSizer.Add(canelBtn2,0,wx.ALIGN_CENTER_VERTICAL)
        
        boxSizer.Add(btnSizer, 0, wx.ALIGN_CENTER, 3)
        self.SetSizer(boxSizer)

    def ShowAbout(self,evt):#�¼�����Ҫ��һ��evt(�¼�)Ϊ����
    	wx.MessageDialog(self,'wxPythonʹ�ý���','��ʾ',wx.OK|wx.ICON_INFORMATION).ShowModal()

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


    def onClose(self,evt):
        self.output.AppendText('close...\r\n')
        time.sleep(1)
        self.Destroy()



class App(wx.App): ##�̳�wx.App
    def OnInit(self): ##��û�е�������ʱ���ȡ��ʼ��
        self.frame = Frame('�޸�host����')        
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