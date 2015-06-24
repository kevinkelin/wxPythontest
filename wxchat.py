#coding:gbk
import wx
import optparse
import time
import threading
import json,pythoncom
import autonet,urllib

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

#�û���
class User():
    def __init__(self,userid="",islogin=0,session=""):        
        self.userid = userid
        self.islogin = islogin
        self.session = session
    
    
class Login(wx.Dialog):
    def __init__(self,NULL,title,user=None):
        wx.Dialog.__init__(self,NULL,title=title,size = (300,200))
        self.user = user
        
        
        #��ʼ�������ı���
        self.useridtext = wx.StaticText(self,-1,"�û�ID")
        self.passtext = wx.StaticText(self,-1,"����")
        self.userid = wx.TextCtrl(self,-1,'',style=wx.TE_LEFT)
        self.password = wx.TextCtrl(self,-1,'',style=wx.TE_PASSWORD)

        #��ʼ��һ��״̬��ʾ�ı���
        self.info = wx.StaticText(self,-1,'')
        
        #��ʼ��������ť
        self.loginBtn = wx.Button(self,-1,"��¼")
        self.Bind(wx.EVT_BUTTON,self.loginuser,self.loginBtn)
        self.regBtn = wx.Button(self,-1,"ע��")
        self.Bind(wx.EVT_BUTTON,self.startReg,self.regBtn)
        self.cancelBtn = wx.Button(self,-1,"�˳�")
        self.Bind(wx.EVT_BUTTON,self.exit,self.cancelBtn)

        #��ʼ��һ��������
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.useridSizer = wx.BoxSizer(wx.HORIZONTAL)        
        self.useridSizer.Add(self.useridtext,1)
        self.useridSizer.Add(self.userid,2)

        self.passSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.passSizer.Add(self.passtext,1)
        self.passSizer.Add(self.password,2)
        
        self.passtext2 = wx.StaticText(self,-1,"�ظ�����")        
        self.password2 = wx.TextCtrl(self,-1,'',style=wx.TE_PASSWORD)
        self.passSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.passSizer2.Add(self.passtext2,1)
        self.passSizer2.Add(self.password2,2)
        

        self.btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btnSizer.Add(self.loginBtn)
        self.btnSizer.Add(self.regBtn)
        self.btnSizer.Add(self.cancelBtn)        

        self.mainSizer.Add((-1,20))
        self.mainSizer.Add(self.useridSizer,2)
        self.mainSizer.Add(self.passSizer,2)
        self.mainSizer.Add(self.passSizer2,2)
        self.passSizer2.Hide(self.passtext2)
        self.passSizer2.Hide(self.password2)
        self.mainSizer.Add(self.info)
        self.mainSizer.Add(self.btnSizer,1)
        
        self.SetSizer(self.mainSizer)

    def loginuser(self,evt):
        userid = self.userid.GetValue()
        userpass = self.password.GetValue()
        self.info.SetLabel(u'������'+userid+u'����ݵ�¼...')
        body=urllib.urlencode({'userId':userid,'pswd':userpass})
        rst = doInThread(autonet.doHttpPost,uri=r"http://pub.releaseoa.corp.qihoo.net:8385/login",body=body)
        while True:
            if not rst.isFinished():
                time.sleep(0.5)
            else:                
                status,headers,contents =  rst.getResult()
                result = json.loads(contents)
                if result['err'] !=0:
                    self.info.SetLabel(result['msg'])
                    break
                else:
                    session =  result['data']['session']                                   
                    self.info.SetLabel(u'��¼�ɹ���seession��'+session)
                    time.sleep(1)
                    print type(userid)
                    self.user.userid = userid
                    self.user.islogin= 1                   
                    self.user.session = session
                    self.Destroy()
                    return self.user
                    

    def startReg(self,evt):
        self.Show(False)
        self.user = User()
        regDig = Reg(self,title="ע��ϵͳ",user = self.user)        
        regDig.Show()
        
    def exit(self,evt):
        self.Destroy()
    
class Reg(Login):
    def __init__(self,Null,title='ע��ϵͳ',user=None):
        Login.__init__(self,Null,title,user)
        # self.user = user
        self.passSizer2.Show(self.passtext2)
        self.passSizer2.Show(self.password2)
        
        #����¼��ע�ᰴť����
        self.btnSizer.Hide(self.regBtn)
        self.btnSizer.Hide(self.loginBtn)
        #�����ע�ᰴť
        self.regBtn = wx.Button(self,-1,"ע��")
        self.Bind(wx.EVT_BUTTON,self.regster,self.regBtn)
        self.btnSizer.Add(self.regBtn)
        
    def regster(self,evt):
        userid = self.userid.GetValue()
        userpass = self.password.GetValue()
        userpass2 = self.password2.GetValue()
        if userpass != userpass2:
            self.info.SetLabel("������������벻һ�£�����������")
            return 
        body = urllib.urlencode({'user':userid,'pswd':userpass})
        rst = doInThread(autonet.doHttpPost,uri=r"http://pub.releaseoa.corp.qihoo.net:8385/register",body=body)
        while True:
            if not rst.isFinished():
                time.sleep(0.5)
            else:                
                status,headers,contents =  rst.getResult()
                newuser = json.loads(contents)
                self.info.SetLabel("ע��ɹ�,��õ���ID��:"+str(newuser['data']['userId'])+',�����˳����¼')
                self.user.userid = newuser['data']['userId']                
                return self.user
            
    def exit(self,evt):
        self.Show(False)
        logDig = Login(self,'��¼ϵͳ')
        logDig.Show()    
        


class Frame(wx.Frame): #Frame ���г�ʼ��
    def __init__(self,title):
        wx.Frame.__init__(self,None,title=title,size = (300,600))
        self.user = User()

        #��ʼ��һ���˵���
        menuBar = wx.MenuBar() 
        
        #��ʼ���������˵���
        loginMenu = wx.Menu() 
        talkMenu = wx.Menu()
        helpMenu = wx.Menu()

        #�ֱ�Ϊ�������˵�������Ӳ˵�
        loginMenu.Append(5001,'��¼')
        loginMenu.AppendSeparator()
        loginMenu.Append(5005,'�ǳ�')
        loginMenu.Enable(5005,False)
        loginMenu.Append(5006,'ע��')
        loginMenu.Append(5009,'E&xit\tAlt+X')

        talkMenu.Append(6001, '�������')        

        helpMenu.Append(7001, '����')

        #����Ӧ�İ�ť��ӷ���
        self.Bind(wx.EVT_MENU,self.startLogin,id=5001)
        self.Bind(wx.EVT_MENU,self.startreg,id=5006)

        #���˵���ӵ�menuBar��
        menuBar.Append(loginMenu,"��¼")
        menuBar.Append(talkMenu,"����")
        menuBar.Append(helpMenu,"����")

        #��menuBar���õ�menu��
        self.SetMenuBar(menuBar)

        #�ڽ����ʼ��һ����ģ��
        self.boxSizer = wx.BoxSizer(wx.VERTICAL)
        #���������ʼ��һ��panel
        self.panel = wx.Panel(self)
        #��panel�����һ��textCtrl
        self.infobox = wx.TextCtrl(self.panel,-1,'',style = wx.TE_MULTILINE|wx.HSCROLL,size=(300,200))
        self.boxSizer.Add(self.panel,1,wx.ALL | wx.EXPAND, 3)        
        self.SetSizer(self.boxSizer)

    def startLogin(self,evt):
        self.infobox.WriteText('start login...')        
        logDig = Login(self,'��¼ϵͳ',user=self.user)        
        logDig.ShowModal()
        self.infobox.AppendText('\r')
        self.infobox.AppendText(self.user.userid+'\r\n')
        self.infobox.AppendText(str(self.user.islogin)+'\r\n')
        self.infobox.AppendText(self.user.session+'\r\n')
        self.listUser(self.user)
        
    def listUser(self,user):
        userid = user.userid
        session = user.session
        body=urllib.urlencode({'userId':userid,'session':session})
        rst = doInThread(autonet.doHttpPost,uri=r"http://pub.releaseoa.corp.qihoo.net:8385/userList",body=body)
        self.tree = wx.TreeCtrl(self.panel,size=(300,500))
        alluser = self.tree.AddRoot(u'�û�')
        onlineitem = self.tree.AppendItem(alluser,u'����')
        offlineitem = self.tree.AppendItem(alluser,u'������')
        
        # offlineId = self.tree.AddRoot(u'����')
        while True:
            if not rst.isFinished():
                time.sleep(0.5)
            else:                
                status,headers,contents =  rst.getResult()
                userlist = json.loads(contents)['data']['userInfoList']
                online = []
                offline = []
                self.userbtn = wx.BoxSizer(wx.VERTICAL)
                for user in userlist:                    
                    if user.get(u'status') == 1:
                        online.append(user)
                    else:
                        offline.append(user)
                        
                for user in online:
                    uid = str(user.get(u'userId'))
                    username = uid+':'+user.get(u'user')                    
                    itemid = self.tree.AppendItem(onlineitem,username)                    
                    self.Bind(wx.EVT_TREE_ITEM_ACTIVATED,self.showSendMessage)
                    # self.Bind(wx.EVT_TREE_ITEM_ACTIVATED,lambda evt,mark =self.tree.GetItemText(itemid): self.showSendMessage(evt,mark),self.tree.GetLastChild(onlineitem))
                    
                for user in offline:
                    uid = str(user.get(u'userId'))
                    username = uid+':'+ user.get(u'user')
                    itemid = self.tree.AppendItem(offlineitem,username)
                    self.Bind(wx.EVT_TREE_ITEM_ACTIVATED,self.showSendMessage)
                    # self.Bind(wx.EVT_TREE_ITEM_ACTIVATED,lambda evt,mark =self.tree.GetItemText(itemid): self.showSendMessage(evt,mark),self.tree.GetLastChild(offlineitem))
                
                self.tree.Expand(onlineitem)   
                
                self.infobox.Hide()
                self.boxSizer.Add(self.tree,3)
                break
        
      
    def startreg(self,evt):
        self.infobox.WriteText('��ʼע�ᡣ����')
        regDig = Reg(self,'ע��ϵͳ',self.user)
        regDig.ShowModal()
        self.infobox.WriteText(user.userid+r'\r\n')
        self.infobox.WriteText(user.islogin+r'\r\n')
        self.infobox.WriteText(user.session+r'\r\n')
        
    def showSendMessage(self,evt):
        treeitemid = evt.GetItem()
        itemtext = self.tree.GetItemText(treeitemid)
        desuid = itemtext.split(":")[0]
        desuser = itemtext.split(":")[1]
        # wx.MessageDialog(self, itemtext,'test2', wx.OK | wx.ICON_INFORMATION).ShowModal()
        title = u'��%s����'%desuser
        chatbox = Chatmsg(self,title,self.user,desuid)
        chatbox.ShowModal()
        
        
class Chatmsg(wx.Dialog):
    def __init__(self,NULL,title,user=None,desuid=""):
        wx.Dialog.__init__(self,NULL,title=title,size = (300,200))
        self.user = user
        self.boxSizer = wx.BoxSizer(wx.VERTICAL)
        self.btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sendBtn = wx.Button(self,-1,u"����")
        self.cacelBtn = wx.Button(self,-1,u"�˳�")
        self.btnSizer.Add(self.sendBtn)
        self.btnSizer.Add(self.cacelBtn)
        self.message = wx.TextCtrl(self,-1,'',style = wx.TE_MULTILINE|wx.HSCROLL,size=(280,150))
        self.boxSizer.Add(self.message,4)
        self.boxSizer.Add(self.btnSizer,1)
        
        self.SetSizer(self.boxSizer)
  
class App(wx.App): ##�̳�wx.App
    def OnInit(self): ##��û�е�������ʱ���ȡ��ʼ��
        self.frame = Frame('QA�ڲ�IM����')        
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