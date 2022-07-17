from unit import *
from  WordPattern import Word
import os
os.chdir('EwtSettings')
t=int(config['time'])
d=config['wordlist']
d=list(d.split(','))
i='M3 U4'
c=loadfileP(i)#c:file object
k=loadjson(json_name='remember_weight.json')

for iii in c[0]:
    IsZero=False
    if (iii.remember_rate==0):
        iii.remember_rate=0.08
        print(iii.words)
    
    
        
savefileP(i,c)