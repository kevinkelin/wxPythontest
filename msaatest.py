# coding:utf-8
"""
该如何形容是好 msaa
"""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'python.zip'))
sys.path.append('safeUI')
import msaa,autoutil,autogui,autoinput,win32gui


if __name__ == '__main__':
    # obj = msaa.window(0)
    # if obj:
        # items = obj.find("ListItem")
        # print items.accName()
        # for item in items:
            # name = item.accName()
            # print name
    # else:
        # print '#######3'
    hwnd360 = autoutil.handleTimeout(autogui.findWindows,5,"DirectUIHWND",parentTitle=u'小工具'.encode('gbk'))
    
    if hwnd360:
        obj = msaa.window(hwnd360[0])
        items = obj.findall("ListItem")        
        for item in items:
            if 'PCHunter32.exe' in item.accName():
                loc =  item.accLocation()
                x,y = msaa.getCoordinate(loc)
                break
        autoinput.clickMouseRight(x,y)
        obj2 = msaa.window("#32768")
        downico = obj2.findall("")
        rolelist = []
        for m in downico:            
            if u'上下文' in m.accName():
                print m.accName()
                dx,dy = msaa.getCoordinate(m.accLocation())
                print dx,dy
                autoinput.moveMouse(dx,dy-50)
                # autoinput.clickMouse(dx,dy)
                break
        
        # items2 = obj2.findall("MenuItem")
        # for i in items2:
            # if u'删除(D)' in i.accName():
                # loc = i.accLocation()
                # print loc
                # x,y = msaa.getCoordinate(loc) #所选择的项所在的坐标
                # desRect = autogui.getDesktopRect()
                # h = desRect[3]
                # if y>h:
                    # print 'y>h'                    
                    # downico = obj2.findall("PopupMenu")
                    # for m in downico:
                        # if u'上下文' in m.accName():
                            # print m.accName()
                            # dx,dy = msaa.getCoordinate(m.accLocation())
                            # print dx,dy
                            # autoinput.moveMouse(dx,dy)
                            # autoinput.clickMouse(dx,dy)
                            
                # else:
                    # print 'y<h'
                    # autoinput.clickMouse(x,y)
                # break
            
    else:
        print 'nothing find'
    
