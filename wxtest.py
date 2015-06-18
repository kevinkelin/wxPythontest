#coding:utf-8
import wx
import optparse

class Frame(wx.Frame): #Frame ���г�ʼ��
    def __init__(self,title):
        wx.Frame.__init__(self,None,title=title,size = (900,700))
        boxSizer = wx.BoxSizer(wx.VERTICAL) #��ʼ��һ��boxSizerģ��

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



        #�������˵�����ӵ�menuBar��
        menuBar.Append(fileMenu,'�ļ�(&F)')
        menuBar.Append(waitMenu, '����(&K)')
        menuBar.Append(helpMenu,'����(&H)')

        #��menuBar��ӵ���Frame��
        self.SetMenuBar(menuBar)

        #��ʼ��һ��panel
        self.panel = wx.Panel(self)
        boxSizer.Add(self.panel,3,wx.ALL|wx.EXPAND,3)

    def ShowAbout(self,evt):#�¼�����Ҫ��һ��evt(�¼�)Ϊ����
    	wx.MessageDialog(self,'wxPythonʹ�ý���','��ʾ',wx.OK|wx.ICON_INFORMATION).ShowModal()

        


class App(wx.App): ##�̳�wx,App
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