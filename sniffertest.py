#coding:gbk
import wx
import optparse
import time
import threading
import os,pcap
       
        
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
        wx.Frame.__init__(self,None,title=title,size = (600,700))
        boxSizer = wx.BoxSizer(wx.VERTICAL)
        filterSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.panel = wx.Panel(self)
        
        # boxSizer.Add(self.panel,1,wx.EXPAND|wx.ALL) #wx.ALL ��Χ�ľ��룬EXPAND���䵽ȫ��
        device = pcap.findalldevs()
        if not device:
            device = ['������ʼ�������⣡']
        ethtext = wx.StaticText(self.panel,-1,"��ѡ������")
        self.ethlist = wx.Choice(self.panel,-1,choices=device,size=(350,20))
        
        filterText = wx.StaticText(self.panel,-1,'����д���˹���')
        hosttext = wx.StaticText(self.panel,-1,'host')
        hostctrl = wx.TextCtrl(self.panel,-1,size=(150,20))
        uritext = wx.StaticText(self.panel,-1,'uri')
        urictrl = wx.TextCtrl(self.panel,-1,size=(100,20))
        self.startButton = wx.Button(self.panel,-1,'��ʼ')        
        self.stopButton = wx.Button(self.panel,-1,'ֹͣ')
        self.stopButton.Disable() #��ֹͣ��ť����Ϊdisable
        self.Bind(wx.EVT_BUTTON,self.start,self.startButton)
        self.Bind(wx.EVT_BUTTON,self.stop,self.stopButton)
        #��д���˹����sizer
        filterSizer.Add(hosttext,0,wx.LEFT|wx.TOP,border=10)
        filterSizer.Add(hostctrl,0,wx.LEFT|wx.TOP,border=10)
        filterSizer.Add(uritext,0,wx.LEFT|wx.TOP,border=10)
        filterSizer.Add(urictrl,0,wx.LEFT|wx.TOP,border=10)
        filterSizer.Add(self.startButton,0,wx.LEFT|wx.TOP,border=10)
        filterSizer.Add(self.stopButton,0,wx.LEFT|wx.TOP,border=10)
        
        #��ʾץ���İ�
        self.sniffer = wx.ListCtrl(self.panel,0,size=(550,450),style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        self.sniffer.InsertColumn(0,'id',format=wx.LIST_FORMAT_LEFT, width=50)
        self.sniffer.InsertColumn(1,'host',format=wx.LIST_FORMAT_LEFT, width=150)
        self.sniffer.InsertColumn(2,'uri',format=wx.LIST_FORMAT_LEFT, width=150)
        
        self.exit = wx.Button(self.panel,-1,'�˳�')
        self.Bind(wx.EVT_BUTTON,self.exitpro,self.exit)
        
        
        boxSizer.Add(ethtext,0,wx.EXPAND|wx.LEFT|wx.TOP,border=10)
        boxSizer.Add(self.ethlist,0,wx.LEFT|wx.TOP,border=10)
        boxSizer.Add(filterText,0,wx.LEFT|wx.TOP,border=10)
        boxSizer.Add(filterSizer,0,wx.LEFT|wx.TOP,border=10)
        boxSizer.Add((-1,20))
        boxSizer.Add(self.sniffer,0,wx.LEFT|wx.TOP,border=10)
        boxSizer.Add(self.exit,0,flag=wx.ALIGN_CENTER|wx.TOP,border=10)
        
        self.panel.SetSizer(boxSizer)
        
    def start(self,evt):
        item = self.ethlist.GetSelection()        
        if item == -1:
            self.message('��ѡ��Ҫץ��������')             
        else:
            eth = self.ethlist.GetString(item)
            self.stopButton.Enable()
            self.startButton.Disable()
            self.exit.Disable()
            print eth
            self.insertinfo(['0','www.360.cn','jijiuxiang.html'])            
            self.insertinfo(['1','www2.360.cn','mygroups?gid=201107190181919446&wvr=6&leftnav=1'])
        
    def stop(self,evt):
        self.stopButton.Disable()
        self.startButton.Enable()
        self.exit.Enable()
        
    def message(self,msg):
        wx.MessageDialog(self,msg, '��ʾ', wx.OK | wx.ICON_INFORMATION).ShowModal()
        
    def insertinfo(self,data):
        row = self.sniffer.GetItemCount()        
        self.sniffer.InsertStringItem(row,str(row+1))
        self.sniffer.SetStringItem(row,1,data[1])
        self.sniffer.SetStringItem(row,2,data[2])
    
    def exitpro(self,evt):
        self.Destroy()
        
        

        

  
class App(wx.App): ##�̳�wx.App
    def OnInit(self): ##��û�е�������ʱ���ȡ��ʼ��
        self.frame = Frame('����sniffer����')
        self.frame.Centre()
        self.frame.Show(True)        
        return True

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