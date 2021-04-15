import os

STYLE = {
        'fore': {
                'black': 30, 'red': 31, 'green': 32, 'yellow': 33,
                'blue': 34, 'purple': 35, 'cyan': 36, 'white': 37,
        },
        'back': {
                'black': 40, 'red': 41, 'green': 42, 'yellow': 43,
                'blue': 44, 'purple': 45, 'cyan': 46, 'white': 47,
        },
        'mode': {
                'bold': 1, 'underline': 4, 'blink': 5, 'invert': 7,
        },
        'default': {
                'end': 0,
        }
}
 
def use_style(string, mode='', fore='', back=''):
    if STYLE['mode'].get(mode):
        mode = '%s' % STYLE['mode'][mode]
    if STYLE['fore'].get(fore):
        fore = '%s' % STYLE['fore'][fore]
    if STYLE['back'].get(back):
        back = '%s' % STYLE['back'][back]
    style = ';'.join([s for s in [mode, fore, back] if s])
    style = '\033[%sm' % style if style else ''
    end = '\033[%sm' % STYLE['default']['end'] if style else ''
    return '%s%s%s' % (style, string, end)

COL=['♠','♣','♥','♦']
NUM=['6 ','7 ','8 ','9 ','10','J ','Q ','K ','A ']

def gaocard(x):
    global COL, NUM
    if x<0: return use_style('?? ',fore='blue',back='white')
    s=COL[x%4]+NUM[x//4]
    if x%4==0: return use_style(s,fore='black',back='white')
    if x%4==1: return use_style(s,mode='bold',fore='black',back='white')
    if x%4==2: return use_style(s,fore='red',back='white')
    if x%4==3: return use_style(s,fore='purple',back='white')
    return s

def UIdoit(data):
    kong='                                      '
    os.system("clear")
    # print(data);print(' ')
    if data['nowturn']<=5:
        print('现在是第 %d 轮\n'%data['nowturn'])
    else:
        print('此局已结束\n')
    for i in range(0,len(data['player'])):
        p=data['player'][i].copy()
        if data['who']==i:
            s=' %d 号位 %s  '%(i,kong[0:max(0,10-len(p['name']))]+use_style(p['name'],mode='bold',back='green'))
        else:
            s=' %d 号位 %s  '%(i,kong[0:max(0,10-len(p['name']))]+use_style(p['name'],mode='bold'))
        if i==data['host']:
            s+=use_style('庄',mode='bold',fore='red',back='yellow')+' '
        else:
            s+='   '
        s+='  %5d / %5d'%(p['inbet'],p['money'])
        if data['nowturn']<=5 and i!=data['who']:
            p['card']=[-1,-1]
        s+='    '+gaocard(p['card'][0])+' '+gaocard(p['card'][1])
        if i==data['nowwho']:
            s+='    正在决策'
        if p['die']==1:
            s+='  已盖牌'
        print(s)
    print(' ')

    if 1:
        c=data['card']
        for i in range(data['nowturn'],5):
            c[i]=-1
        s='公共牌：'
        for i in range(0,5):
            s+=' '+gaocard(c[i])
        print(s)
        print(' ')
    
    print(data['logs'])
    print(' ')
    if data['wait']==1:
        print('（请输入）')
    return 0


# tmp=''
# for i in range(-1,36): tmp+=gaocard(i)+' '
# print(tmp)