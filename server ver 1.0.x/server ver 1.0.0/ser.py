from flask import Flask , session , request , send_from_directory
from calcvalue import *
import os, random

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

pswdtoname={}
gamestarted=0
orginmoney=100

@app.route('/reg',methods=["post"])
def approutereg():
    A=request.form.get('A'); B=request.form.get('B')
    global pswdtoname, gamestarted
    if gamestarted:
        return '404'
    pswdtoname[A]=B
    print(B+" is registed")
    return 'ok'

@app.route('/pre',methods=["post"])
def approutepre():
    A=request.form.get('A'); B=request.form.get('B')
    global pswdtoname, gamestarted
    if gamestarted:
        return 'started'
    usn=[]
    for pswd in pswdtoname:
        usn.append(pswdtoname[pswd])
    return "现在玩家有："+str(usn)

UIid=0
n=0
player=[]
nowsta=''
tbit=[]
all0=[]
logs=''
nowturn=6
nowwho=0
card=[-1,-1,-1,-1,-1]
host=0

def getplayerid(s):
    global UIid, n, player, nowsta, tbit, all0, logs, nowturn, nowwho, card, host
    for i in range(0,n):
        if player[i]['pswd']==s:
            return i
    return -1

def newround():
    global UIid, n, player, nowsta, tbit, all0, logs, nowturn, nowwho, card, host
    UIid+=1
    nowwho=-1
    for i in range(0,n):
        if player[i]['money']>0:
            tbit[i]=1
        else:
            tbit[i]=0
    nowsta='waitallplayer'
    return 0

def gotowin(w):
    global UIid, n, player, nowsta, tbit, all0, logs, nowturn, nowwho, card, host
    UIid+=1
    nowturn=6
    lim=player[w]['inbet']
    tot=0
    for i in range(0,n):
        player[i]['inbet']=min(lim,player[i]['inbet'])
        player[i]['money']-=player[i]['inbet']
        tot+=player[i]['inbet']
        player[i]['inbet']=0
    player[w]['money']+=tot
    logs='%d 号位的 %s 赢了 %d\n' % (w,player[w]['name'],tot)
    newround()
    return 0

def pickcard():
    global UIid, n, player, nowsta, tbit, all0, logs, nowturn, nowwho, card, host
    x=card[0]
    del(card[0])
    return x

def findnext(x):
    global UIid, n, player, nowsta, tbit, all0, logs, nowturn, nowwho, card, host
    while 1:
        x=(x+1)%n
        if player[x]['die']==0:
            return x
    return -1

def dobet(w,v):
    global UIid, n, player, nowsta, tbit, all0, logs, nowturn, nowwho, card, host
    UIid+=1
    player[w]['inbet']+=v
    if player[w]['inbet']>player[w]['money']:
        player[w]['inbet']=player[w]['money']
    return 0

def setturn(turn):
    global UIid, n, player, nowsta, tbit, all0, logs, nowturn, nowwho, card, host
    UIid+=1
    if turn>5:
        winner=-1
        mxv=-1
        for ii in range(0,n):
            i=(host+ii+1)%n
            if player[i]['die']==0:
                v=calcvalue(player[i]['card']+card)
                if v>=mxv:
                    mxv=v
                    winner=i
        gotowin(winner)
        return 1

    for i in range(0,n):
        if player[i]['die']:
            tbit[i]=0
        else:
            tbit[i]=1
    nowturn=turn
    nowwho=findnext(host)
    if turn==0:
        dobet(nowwho,1)
        nowwho=findnext(nowwho)
        dobet(nowwho,2)
        nowwho=findnext(nowwho)
    return 0

def maxbet():
    global UIid, n, player, nowsta, tbit, all0, logs, nowturn, nowwho, card, host
    mx=0
    for i in range(0,n):
        mx=max(mx,player[i]['inbet'])
    return mx

def balance():
    global UIid, n, player, nowsta, tbit, all0, logs, nowturn, nowwho, card, host
    mx=maxbet()
    for i in range(0,n):
        if player[i]['die']==0 and player[i]['money']!=player[i]['inbet'] and player[i]['inbet']<mx:
            return 0
    return 1

def fold(w):
    global UIid, n, player, nowsta, tbit, all0, logs, nowturn, nowwho, card, host
    nowwho=findnext(nowwho)
    UIid+=1
    player[w]['die']=1
    vec=[]
    for i in range(0,n):
        if player[i]['die']==0:
            vec.append(i)
    if len(vec)==1:
        gotowin(vec[0])
        return 1
    tbit[w]=0
    return 0

def gobet(w,v):
    global UIid, n, player, nowsta, tbit, all0, logs, nowturn, nowwho, card, host
    nowwho=findnext(nowwho)
    UIid+=1
    if player[w]['inbet']+v<maxbet():
        v=maxbet()-player[w]['inbet']
    dobet(w,v)
    tbit[w]=0
    if tbit==all0 and balance():
        if nowturn==0:
            setturn(3)
        else:
            setturn(nowturn+1)
        return 1
    return 0

def newround2():
    global UIid, n, player, nowsta, tbit, all0, logs, nowturn, nowwho, card, host
    UIid+=1
    nowsta='playing'
    card=[]
    for i in range(0,36):
        card.append(i)
    random.shuffle(card)
    host=findnext(host)
    for i in range(0,n):
        if player[i]['money']<=0:
            player[i]['die']=1
            continue
        else:
            player[i]['die']=0
        player[i]['card'][0]=pickcard()
        player[i]['card'][1]=pickcard()
    while len(card)>5: pickcard()
    logs=''
    logs+='庄家是 %d 号位的 %s\n' % (host,player[host]['name'])
    logs+='小盲是 %d 号位的 %s\n' % (findnext(host),player[findnext(host)]['name'])
    logs+='大盲是 %d 号位的 %s\n' % (findnext(findnext(host)),player[findnext(findnext(host))]['name'])
    setturn(0)
    return 0

@app.route('/start',methods=["post"])
def approutestart():
    global UIid, n, player, nowsta, tbit, all0, logs, nowturn, nowwho, card, host
    A=request.form.get('A'); B=request.form.get('B')
    global gamestarted
    if gamestarted:
        return 'fxxk'
    gamestarted=1
    for pswd in pswdtoname:
        n+=1
        player.append({})
        player[n-1]['pswd']=pswd
        player[n-1]['name']=pswdtoname[pswd]
        player[n-1]['money']=orginmoney
        player[n-1]['inbet']=0
        player[n-1]['card']=[-1,-1]
        player[n-1]['die']=0
        tbit.append(0)
    all0=tbit.copy()
    newround()
    return 'ok'

@app.route('/getuiid',methods=["post"])
def approutegetuiid():
    global UIid, n, player, nowsta, tbit, all0, logs, nowturn, nowwho, card, host
    return str(UIid)

@app.route('/getui',methods=["post"])
def approutegetui():
    global UIid, n, player, nowsta, tbit, all0, logs, nowturn, nowwho, card, host
    A=request.form.get('A'); B=request.form.get('B')
    w=getplayerid(A)
    res={}
    res['wait']=0
    res['player']=player.copy()
    res['logs']=logs
    res['card']=card.copy()
    res['who']=w
    res['nowturn']=nowturn
    res['nowwho']=nowwho
    res['host']=host
    
    if nowsta=='waitallplayer':
        res['wait']=tbit[w]
        if tbit[w]:
            res['logs']+='    上一局已经结束，请输入任意字符串\n'
        return str(res)
    
    if nowsta=='playing':
        if w==nowwho:
            res['wait']=1
        res['logs']+='    （f盖牌，否则输入任意自然数x表示自己赌注+=x）\n'
        return str(res)

    return "{'wait':0}"

def takeint(s):
    x=0
    for c in s:
        if c>='0' and c<='9':
            x=x*10+ord(c)-ord('0')
    return x

@app.route('/opt',methods=["post"])
def approuteopt():
    global UIid, n, player, nowsta, tbit, all0, logs, nowturn, nowwho, card, host
    UIid+=1
    A=request.form.get('A'); B=request.form.get('B')
    w=getplayerid(A)
    if nowsta=='waitallplayer':
        tbit[w]=0
        if tbit==all0:
            newround2()
        return 'ok'
    if nowsta=='playing':
        if w==nowwho:
            if B[0]=='F' or B[0]=='f':
                fold(w)
            else:
                gobet(w,takeint(B))
        else:
            return 'fxxk'

    return 'fxxk'

if __name__=='__main__':
    print('输入初始金额（推荐 20-100）：')
    orginmoney=int(input())
    print('输入端口号（推荐 5000）：')
    pt=int(input())
    app.run(host='0.0.0.0',port=pt)