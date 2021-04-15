sgm=9

def gaosort(a):
    res=0
    for i in range(0,5):
        res+=a[i]*(100**i)
    return res

def gaogaopai(a):
    for i in range(0,5):
        a[i]=a[i]//4
    a.sort()
    return gaosort(a)

def gaoyidui(a):
    global sgm
    tong=[]
    for i in range(0,sgm):
        tong.append(0)
    for i in range(0,5):
        tong[a[i]//4]+=1
    for i in range(0,sgm):
        if tong[i]==2:
            tong[i]=0
            b=[]
            for k in range(0,sgm):
                while tong[k]>0:
                    tong[k]-=1
                    b.append(k)
            b.append(i)
            b.append(i)
            return gaosort(b)
    return 0


def gaoliangdui(a):
    global sgm
    tong=[]
    for i in range(0,sgm):
        tong.append(0)
    for i in range(0,5):
        tong[a[i]//4]+=1
    for i in range(0,sgm):
        for j in range(i+1,sgm):
            if tong[i]==2 and tong[j]==2:
                tong[i]=0; tong[j]=0
                b=[]
                for k in range(0,sgm):
                    while tong[k]>0:
                        tong[k]-=1
                        b.append(k)
                b.append(i)
                b.append(i)
                b.append(j)
                b.append(j)
                return gaosort(b)
    return 0

def gaosantiao(a):
    global sgm
    tong=[]
    for i in range(0,sgm):
        tong.append(0)
    for i in range(0,5):
        tong[a[i]//4]+=1
    for i in range(0,sgm):
        if tong[i]==3:
            tong[i]=0
            b=[]
            for k in range(0,sgm):
                while tong[k]>0:
                    tong[k]-=1
                    b.append(k)
            b.append(i)
            b.append(i)
            b.append(i)
            return gaosort(b)
    return 0   

def gaositiao(a):
    global sgm
    tong=[]
    for i in range(0,sgm):
        tong.append(0)
    for i in range(0,5):
        tong[a[i]//4]+=1
    for i in range(0,sgm):
        if tong[i]==4:
            tong[i]=0
            b=[]
            for k in range(0,sgm):
                while tong[k]>0:
                    tong[k]-=1
                    b.append(k)
            b.append(i)
            b.append(i)
            b.append(i)
            b.append(i)
            return gaosort(b)
    return 0   

def gaohulu(a):
    global sgm
    tong=[]
    for i in range(0,sgm):
        tong.append(0)
    for i in range(0,5):
        tong[a[i]//4]+=1
    for i in range(0,sgm):
        for j in range(0,sgm):
            if tong[i]==3 and tong[j]==2:
                tong[i]=0; tong[j]=0
                b=[]
                for k in range(0,sgm):
                    while tong[k]>0:
                        tong[k]-=1
                        b.append(k)
                b.append(j)
                b.append(j)
                b.append(i)
                b.append(i)
                b.append(i)
                return gaosort(b)
    return 0

def gaotonghua(a):
    for i in range(1,5):
        if a[i]%4!=a[0]%4:
            return 0
    return gaogaopai(a.copy())

def gaoshunzi(a):
    for i in range(0,5):
        a[i]=a[i]//4
    a.sort()
    for i in range(1,5):
        if a[i]!=a[i-1]+1:
            return 0
    return gaosort(a)

def gao5(a):
    bas=10000000000000000000
    tonghua=gaotonghua(a.copy())
    shunzi=gaoshunzi(a.copy())
    if shunzi>0 and tonghua>0: return bas*9+shunzi
    sitiao=gaositiao(a.copy())
    if sitiao>0: return bas*8+sitiao
    hulu=gaohulu(a.copy())
    if hulu>0: return bas*7+hulu
    if tonghua>0: return bas*6+tonghua
    if shunzi>0: return bas*5+shunzi
    santiao=gaosantiao(a.copy())
    if santiao>0: return bas*4+santiao
    liangdui=gaoliangdui(a.copy())
    if liangdui>0: return bas*3+liangdui
    yidui=gaoyidui(a.copy())
    if yidui>0: return bas*2+yidui
    return bas*1+gaogaopai(a.copy())


def calcvalue(a):
    res=0
    for S in range(0,2**len(a)):
        b=[]
        for i in range(0,len(a)):
            if S//(2**i)%2==1:
                b.append(a[i])
        if len(b)==5:
            res=max(res,gao5(b))
    return res
