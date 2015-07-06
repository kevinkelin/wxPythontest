#coding:gbk
import wx
import optparse
import time
import threading
import os,pcap,httpsniffer,re

       
id = 0
result = []        
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
        wx.Frame.__init__(self,None,title=title,size = (600,700))
        boxSizer = wx.BoxSizer(wx.VERTICAL)
        filterSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.panel = wx.Panel(self)
        
        # boxSizer.Add(self.panel,1,wx.EXPAND|wx.ALL) #wx.ALL 周围的距离，EXPAND扩充到全部
        device = pcap.findalldevs()
        if not device:
            device = ['网卡初始化有问题！']
        ethtext = wx.StaticText(self.panel,-1,"请选择网卡")
        self.ethlist = wx.Choice(self.panel,-1,choices=device,size=(350,20))
        
        filterText = wx.StaticText(self.panel,-1,'请书写过滤规则')
        hosttext = wx.StaticText(self.panel,-1,'host')
        self.hostctrl = wx.TextCtrl(self.panel,-1,size=(150,20))
        uritext = wx.StaticText(self.panel,-1,'uri')
        self.urictrl = wx.TextCtrl(self.panel,-1,size=(100,20))
        self.startButton = wx.Button(self.panel,-1,'开始')        
        self.stopButton = wx.Button(self.panel,-1,'停止')
        self.stopButton.Disable() #将停止按钮设置为disable
        self.Bind(wx.EVT_BUTTON,self.start,self.startButton)
        self.Bind(wx.EVT_BUTTON,self.stop,self.stopButton)
        #书写过滤规则的sizer
        filterSizer.Add(hosttext,0,wx.LEFT|wx.TOP,border=10)
        filterSizer.Add(self.hostctrl,0,wx.LEFT|wx.TOP,border=10)
        filterSizer.Add(uritext,0,wx.LEFT|wx.TOP,border=10)
        filterSizer.Add(self.urictrl,0,wx.LEFT|wx.TOP,border=10)
        filterSizer.Add(self.startButton,0,wx.LEFT|wx.TOP,border=10)
        filterSizer.Add(self.stopButton,0,wx.LEFT|wx.TOP,border=10)
        
        #显示抓到的包
        self.sniffer = wx.ListCtrl(self.panel,0,size=(550,450),style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        self.sniffer.InsertColumn(0,'id',format=wx.LIST_FORMAT_LEFT, width=50)
        self.sniffer.InsertColumn(1,'host',format=wx.LIST_FORMAT_LEFT, width=150)
        self.sniffer.InsertColumn(2,'uri',format=wx.LIST_FORMAT_LEFT, width=150)
        
        self.exit = wx.Button(self.panel,-1,'退出')
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
            self.message('请选择要抓包的网卡')             
        else:
            eth = self.ethlist.GetString(item)            
            self.stopButton.Enable()
            self.startButton.Disable()
            self.exit.Disable()
            hostfilter = self.hostctrl.GetValue()
            urifilter = self.urictrl.GetValue()
            pc = pcap.pcap(eth) #初始化pc
            filter = r'tcp'
            pc.setfilter(filter)
            doInThread(pc.loop,self.process,hostfilter,urifilter)
            
            
        
    def stop(self,evt):
        self.stopButton.Disable()
        self.startButton.Enable()
        self.exit.Enable()
        
        
    def message(self,msg):
        wx.MessageDialog(self,msg, '提示', wx.OK | wx.ICON_INFORMATION).ShowModal()
        
    def insertinfo(self,data):
        row = self.sniffer.GetItemCount()        
        self.sniffer.InsertStringItem(row,str(row+1))
        self.sniffer.SetStringItem(row,1,data[2])
        self.sniffer.SetStringItem(row,2,data[3])
    
    def exitpro(self,evt):
        self.Destroy()    
    
    def process(self,ts, pkt,hostfilter='',urifilter=''):
        global id, result        
        if not hostfilter:
            hostfilter = r'.*?360.*?'
        if not urifilter:
            urifilter = r'.*?'
        try:
            h = httpsniffer.HttpHandler()
            r = h.process(ts, pkt)
            if r:
                data = r.getdata()
                
                if not data[1]:
                    return
                if (re.match(hostfilter,data[1]) and re.match(r'http',data[0],re.I) and re.match(urifilter,data[2])) or urifilter in data[2]:
                    id += 1
                    data.insert(0, str(id))
                    result.append(data)
                    print data
                    self.insertinfo(data)              
        except:
            pass
  
class App(wx.App): ##继承wx.App
    def OnInit(self): ##还没有调起来的时候读取初始化
        self.frame = Frame('简易sniffer工具')
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