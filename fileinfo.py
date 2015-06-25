#coding:gbk
import wx
import optparse
import time,hashlib
import threading
import os


def checkMD5(pefile):
    try:
        f = open(pefile,'rb')
        data = f.read()
        m = hashlib.md5()
        m.update(data)
        f.close()
        return m.hexdigest()
    except:
        return 'error'
    
def getFileSize(filename):
    try:
        size = int(os.path.getsize(filename))
        return size
    except:
        return 'error'



        
        
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

class FileDropTarget(wx.FileDropTarget):
    def __init__(self, filetext,md5tx,filesizetx):
        wx.FileDropTarget.__init__(self)
        self.filepath = filetext
        self.md5tx = md5tx
        self.filesizetx = filesizetx
        

    def OnDropFiles(self,  x,  y, fileNames):
        filename = fileNames[0].encode('gbk')
        print filename
        print type(filename)
        self.filepath.SetValue(filename)
        md5 = doInThread(checkMD5,filename)
        filesize = doInThread(getFileSize,filename)
        while True:
            if not md5.isFinished():
                time.sleep(0.5)
            else:
                self.md5tx.SetValue(md5.getResult())
                break
                
        while True:
            if not filesize.isFinished():
                time.sleep(0.5)
            else:
                self.filesizetx.SetValue(str(filesize.getResult()))
                break
                    
        
        


class Frame(wx.Frame): #Frame 进行初始化
    def __init__(self,title):
        wx.Frame.__init__(self,None,title=title,size = (400,300))
        boxSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.panel = wx.Panel(self)
        
        # boxSizer.Add(self.panel,1,wx.EXPAND|wx.ALL) #wx.ALL 周围的距离，EXPAND扩充到全部
        
        filepath = wx.StaticText(self.panel,-1,"FileDir(请将文件拖到本对话框中)")
        filetext = wx.TextCtrl(self.panel,-1,"",size=(350,20))
        
        md5st = wx.StaticText(self.panel,-1,"MD5")
        md5tx = wx.TextCtrl(self.panel,-1,size=(250,20))
        
        filesizest = wx.StaticText(self.panel,-1,'FileSize')
        filesizetx = wx.TextCtrl(self.panel,-1,size=(250,20))
        
        # hashst = wx.StaticText(self.panel,-1,'Hash')
        # hashtx = wx.TextCtrl(self.panel,-1,size=(250,20))
        
        boxSizer.Add(filepath,0,wx.EXPAND|wx.LEFT|wx.TOP,border=10)
        boxSizer.Add(filetext,0,wx.LEFT|wx.TOP,border=10)
        boxSizer.Add((-1,20))
        boxSizer.Add(md5st,0,wx.LEFT|wx.TOP,border=10)
        boxSizer.Add(md5tx,0,wx.LEFT|wx.TOP,border=10)
        boxSizer.Add((-1,10))
        boxSizer.Add(filesizest,0,wx.LEFT|wx.TOP,border=10)
        boxSizer.Add(filesizetx,0,wx.LEFT|wx.TOP,border=10)
        # boxSizer.Add((-1,10))
        # boxSizer.Add(hashst,0,wx.LEFT|wx.TOP,border=10)
        # boxSizer.Add(hashtx,0,wx.LEFT|wx.TOP,border=10)
        
        dropTarget = FileDropTarget(filetext,md5tx,filesizetx)
        self.panel.SetDropTarget( dropTarget )
        
        self.panel.SetSizer(boxSizer)
        
        

        

  
class App(wx.App): ##继承wx.App
    def OnInit(self): ##还没有调起来的时候读取初始化
        self.frame = Frame('MD5&size信息')        
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