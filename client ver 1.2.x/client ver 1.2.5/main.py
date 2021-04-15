import os, random, time
from UI import *

def ipt():
    while 1:
        s=input()
        if len(s)>0:
            return s
    return ''

pswd=str(random.random())
serip=''
if 1:
    os.system('touch ipconfig')
    f=open('ipconfig','r')
    tmp=f.read().split('\n')
    if len(tmp)>0:
        serip=tmp[0]
        print("是否使用ipconfig中的ip（%s）作为服务器地址？（回答y/n）"%serip)
        while 1:
            s=input()
            if s=='y' or s=='Y':
                break
            else:
                serip=''
                break

if len(serip)==0:
    print("请输入服务器地址（形如http://xxxxxxxx:yyyy）：")
    serip=ipt()

print("请输入您的用户名：")
name=ipt()

lastuiid=-1
lastui={}

def con(s,A='',B=''):
    # return connect(s,A=A,B=B)
    res=''
    os.system("touch connect.out")
    os.system("./connect \"%s\" \"%s\" \"%s\""%(s,A,B))
    if 1:
        f=open('connect.out','r')
        res=f.read()
    return res

def magiccon(s,A='',B=''):
    global lastuiid, lastui
    while 1:
        res=con(s,A=A,B=B)
        if res!='':
            return res
        if lastuiid>=0:
            UIdoit(lastui.copy())
        time.sleep(0.1)
    return ''

def paintui():
    global lastui, lastuiid
    if int(magiccon(serip+'/getuiid'))==lastuiid:
        return 0
    lastuiid=int(magiccon(serip+'/getuiid'))
    lastui=eval(magiccon(serip+'/getui',A=pswd))
    UIdoit(lastui.copy())
    return 0

if magiccon(serip+'/reg',A=pswd,B=name)=='404':
    print("114514 can't join in. The 1919810 has begun")
    exit(0)

while 1:
    t=magiccon(serip+'/pre')
    if (t=='started'):
        break
    os.system("clear")
    print(t)
    print("    输入's'开始游戏，否则刷新")
    s=ipt()
    if s=='s':
        magiccon(serip+'/start')

print('Game Starting')

while 1:
    time.sleep(0.2)
    paintui()
    if lastui['wait']==1:
        t=ipt()
        magiccon(serip+'/opt',A=pswd,B=t)
