#coding:gbk
"""
网络请求自动化方法
"""

import sys, time
import httplib
import smtplib
import ctypes

#---------------------------------------------------------------------------------------------
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE= -11
STD_ERROR_HANDLE = -12

FOREGROUND_WHITE = 0x0007
FOREGROUND_BLUE = 0x01 # text color contains blue.
FOREGROUND_GREEN= 0x02 # text color contains green.
FOREGROUND_RED  = 0x04 # text color contains red.
FOREGROUND_INTENSITY = 0x08 # text color is intensified.
FOREGROUND_YELLOW = FOREGROUND_RED | FOREGROUND_GREEN

BACKGROUND_BLUE = 0x10 # background color contains blue.
BACKGROUND_GREEN= 0x20 # background color contains green.
BACKGROUND_RED  = 0x40 # background color contains red.
BACKGROUND_INTENSITY = 0x80 # background color is intensified.

std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

#在try中执行
def tryExcept(func, *params, **paramMap):
    try:
        return func(*params, **paramMap)
    except Exception, e:
        return e

#从uri中分离出host和location
def parseUri(uri):
    index1 = uri.find('://') + 3
    index2 = uri.find('/', index1)
    if index2 == -1:
        return uri[index1:], '/'
    return uri[index1:index2], uri[index2:]

#http的get请求
def doHttpGet(uri, headers = {}):
    return doHttp(uri, 'GET', None, headers)

#http的post请求
def doHttpPost(uri, body, headers = {}):
    return doHttp(uri, 'POST', body, headers)

def getHttpFileSize(uri):
    def getRedirectUrl(response_headers):
        for k, v in response_headers:
            if k == 'location':
                return v
        
    host, location = parseUri(uri)
    baseHeaders = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': host,
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7'
    }
    conn = None
    try:
        conn = httplib.HTTPConnection(host)
        conn.request('GET', location, None, baseHeaders)
        res = conn.getresponse()
        if res.status in [301, 302, 303]:
            location = getRedirectUrl(res.getheaders())
            return location
        for k, v in res.getheaders():
            if k == 'content-length':
                return int(v)
    except Exception, e:
        import traceback
        print traceback.format_exc()
        return
    finally:
        if conn:
            tryExcept(conn.close)

#http请求
def doHttp(uri, method, body, headers = {}):
    host, location = parseUri(uri)
    baseHeaders = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': host,
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7'
    }
    if headers:
        for k, v in headers.items():
            baseHeaders[k] = v
    conn = None
    try:
        conn = httplib.HTTPConnection(host)
        conn.request(method, location, body, headers)
        res = conn.getresponse()
        headers = {}
        for k, v in res.getheaders():
            headers[k] = v
        return res.status, headers, res.read()
    except Exception, e:
        return e
    finally:
        if conn:
            tryExcept(conn.close)
            

def set_color(color, handle=std_out_handle):
    bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return bool
            
def _print(_str, color=FOREGROUND_WHITE):
    set_color(color)
    sys.stdout.write(_str+'\n')
    sys.stdout.flush()
    set_color(FOREGROUND_WHITE)
    
#获取当前时间戳
def getTime(style = '%Y-%m-%d %H:%M:%S'):
    return time.strftime(style, time.localtime())

def sendMail(mail_from, mail_to, mail_title, mail_content, mail_server=r'mail.corp.qihoo.net', mail_port=25):
    try:
        handle = smtplib.SMTP(mail_server, mail_port)
        #handle = smtplib.SMTP('mail.360.cn', 25)
        handle.ehlo()  
        handle.starttls()  
        handle.ehlo()  

        mail_data = getTime()

        msg = "From: %s\r\nTo: %s\r\nData: %s\r\nContent-Type: text/html;charset=gb2312\r\nSubject: %s \r\n\r\n %s\r\n"  % (mail_from, str(mail_to).replace('[', '').replace(']', ''), mail_data, mail_title, mail_content)
        handle.sendmail('%s' % mail_from, mail_to, msg)
        handle.close()
    except Exception, e:
        _print('sendMail: '+str(e), FOREGROUND_RED|FOREGROUND_INTENSITY)
        print '发信失败,程序退出...'
        
if __name__ == '__main__':
##    sendMail('autotest@360.cn', 'hanjingjing@360.cn', 'test', 'test')
    ret = getHttpFileSize(r'http://sd.360.cn/downloadbeta.html')
    ret = getHttpFileSize(ret)
    print type(ret), ret, 111111111