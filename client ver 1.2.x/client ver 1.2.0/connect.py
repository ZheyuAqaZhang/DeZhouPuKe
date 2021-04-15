import requests, sys

a=sys.argv
a.append('')
a.append('')
a.append('')

if 1:
    f=open('connect.out','w')
    f.write('')
r = requests.post(url=a[1],data={'A':a[2],'B':a[3]},timeout=0.2)
if 1:
    f=open('connect.out','w')
    f.write(r.text)
