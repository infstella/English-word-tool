import threading
import playsound
#from playsound import playsound
import Play_mp3 
import time,pickle,json,os
#from winsound import PlaySound

#import pygame
from WordPattern import *
import sys
from Youdao_Pronunciation import youdao

#from win32com.client import constants
#import win32com.client 
#import pyttsx3
#Listnum=1

print('456')
font=('宋体', 20)
FONT=('黑体', 12)
MICROFONT=('黑体', 12)
HEADFONT=FONT=('宋体', 22)
global filename
filename='M2 Words'
#filename='WordsList'
CHOOSE_NORMAL=0
CHOOSE_OLD=1
CHOOSE_NEW=2
LOCAL_SOFTWARE_VERSION='v0.1'
yd=youdao()

#yd=None
#engine = pyttsx3.init() # object creation

class Logger(object):
    def __init__(self, fileN='Terminal.log'):
        self.terminal = sys.stdout
        
        try:
            self.log = open(fileN, 'a')
        except FileNotFoundError:
            open(fileN,'w')
            self.log = open(fileN, 'a')
        self.messageCache=''
        self.log.write('\n\n\n')

    def write(self, message):
        '''print实际相当于sys.stdout.write'''
        self.terminal.write(message)
        nowTime=str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        if message!='\n':
            self.messageCache+=message
        else:
            self.log.write(nowTime+':    '+self.messageCache+'\n')
            self.messageCache=''

    def flush(self):
        pass


sys.stdout = Logger()#'G:/2.0/test.txt'

  
'''def dec86400(num):
    mid=[]
    while True:
        if num == 0: break
        mid.append(num%86400)
        num=num//86400

    return int(''.join([str(x) for x in mid[::-1]]))//100000'''

def dec86400P(num):
    return num//86400

#today_date:date ; timedate:calculable  
def creat():
    global TotalList
    TotalList=[[],{'version':'v0.2','num_version':2}]
    TotalList[0].append(Word(words='hello',chinese='哈喽',create_time=today_date,forget_time='2021-12-15',wordlist='NewWordsList'))
    TotalList[0].append(Word(words='world',chinese='世界',create_time=today_date,forget_time='2021-12-16',wordlist='NewWordsList'))

def loadjson(json_name='config.json'):
    f = open(json_name, 'r')
    content = f.read()
    a = json.loads(content)
    f.close()
    return a

def savejson(x,json_name='config.json'):
    b = json.dumps(x,sort_keys=True, indent=4)
    f2 = open(json_name, 'w')
    f2.write(b)
    f2.close()

def PrintLog(content,IsTime=True,logName='Default.log',IsReflash=False):
    if IsReflash:
        f2 = open(logName, 'w')
        f2.write('')
        f2.close()

    f2 = open(logName, 'a')
    nowTime=str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    f2.write(nowTime+':    '+str(content)+'\n')
    f2.close()

def loadfile(filename):
    global TotalList
    with open('wordlist//'+filename+'.wl', 'rb') as fp:
        TotalList = pickle.load(fp)
        print(len(TotalList[1]))
        
def loadfileP(filename):
    with open('wordlist//'+filename+'.wl', 'rb') as fp:
        list1=pickle.load(fp)
    return list1

#loadfile(filename)
def chooseWords(x,type,InpList):
    i=0
    ii=0
    rlist=[]
    while ii<=x and i<=len(InpList)-1:
        c=InpList[i]
        if c.remember_rate<0.4 and type==CHOOSE_NORMAL:
            rlist.append(c)
            ii+=1

        if 0.05<c.remember_rate<0.49 and type==CHOOSE_OLD:
            rlist.append(c)
            ii+=1
        
        if c.remember_rate<0.05 and type==CHOOSE_NEW:
            rlist.append(c)
            ii+=1

        i+=1
    return rlist



def f(x):
    if x>0.15:
        return -1.32**(-x)+0.96
    else:
        return 1

def forget():
    for i in range(len(TotalList)):
        #a=f(timedate-dSTN(i.forget_time))
        i.remember_rate=i.remember_rate*f(timedate-dSTN(i.forget_time))

def dSTN(str1):#StrdateToNumdate
    timeArray = time.strptime(str1, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    return dec86400P(timeStamp)
a=dSTN('2021-12-18')

def checkinit():
    try:
        f = open('config.json', 'r')
    except:
        x={"Old": "0", "New": "0", "wordlist": "", "time": 0}
        open('config.json','w')
        b = json.dumps(x)
        f2 = open('config.json', 'w')
        f2.write(b)
        f2.close()
        os.mkdir("wordlist")
    try:
        f = open('remember_weight.json', 'r')
    except:
        x={"NewWordsList": 1}
        open('remember_weight.json','w')
        savejson(x,json_name='remember_weight.json')
checkinit()




timeStamp = time.time()
time_time = time.strftime('%Y-%m-%d', time.localtime(timeStamp))
print('now time:',time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timeStamp)))
timeArray = time.strptime(time_time, "%Y-%m-%d")
timeStamp = int(time.mktime(timeArray))
today_date = time.strftime('%Y-%m-%d', time.localtime(timeStamp))
timedate=dec86400P(int(timeStamp))
global config
config=loadjson()
global TotalList
TotalList=[]
try:
    with open('wordlist//'+'NewWordsList.wl', 'rb') as fp:  # 把 t 对象从文件中读出来，并赋值给 t2
        a=TotalList
        TotalList1 = pickle.load(fp)
        TotalList = TotalList1
except FileNotFoundError:
    creat()
    filename='NewWordsList'
    with open('wordlist//'+'NewWordsList.wl', 'w+b') as fp: # 把 t 对象存到文件中
        #global TotalList
        pickle.dump(TotalList, fp)

def get_all_file():
    wordlistname=[]
    for roott, dirs, files in os.walk((os.getcwd()+'//wordlist')):
        for item in files:  
            if (item.split('.')[-1]=='wl'):
                a=item.split('.')[0]
                wordlistname.append(item.split('.')[0]) #os.walk()所在目录的所有非目录文件名
        a=dirs
        a=roott
    return list(set(wordlistname))
    
#get_all_file()
def start():
    checkinit()  
    checkforget()
    Speak_init()
    ResetWordlist()
    #[name,wl]



def savefile():
    with open('wordlist//'+filename+'.wl', 'w+b') as fp: # 把 t 对象存到文件中
        pickle.dump(TotalList, fp)
        
def savefileP(filename,item):
    with open('wordlist//'+filename+'.wl', 'w+b') as fp: # 把 t 对象存到文件中
        pickle.dump(item, fp)

def Asavefile():
    for i in a:
        with open('wordlist//'+i+'.wl', 'w+b') as fp: # 把 t 对象存到文件中
            pickle.dump(TotalList, fp)

def checkforget():
    
    t=int(config['time'])
    d=config['wordlist']
    d=list(d.split(','))
    
    

    if timedate != t and config['wordlist']!='':
        PrintLog('',logName='checkforget.log',IsReflash=True)
        config['time']=timedate
        for i in d:#i: file name
            
            c=loadfileP(i)#c:file object
            k=loadjson(json_name='remember_weight.json')
            try:
                weight=k[i]#k: extra weight
            except KeyError:
                k[i]=1
                weight=1
                savejson(k,json_name='remember_weight.json')
            for iii in c[0]:
                cachenum=iii.remember_rate
                d= 1-(weight*(1- f (timedate-dSTN(iii.forget_time) ) ) )
                iii.remember_rate=iii.remember_rate*  1-(weight*(1- f (timedate-dSTN(iii.forget_time) ) ) )#update remenber rate
                if iii.remember_rate<0:
                    iii.remember_rate=0
                PrintLog((str(iii.words)+' '+str(d)+': '+str(cachenum)+'-->'+str(iii.remember_rate)),logName='checkforget.log')
            savefileP(i,c)
            #with open('wordlist//'+i, 'w+b') as fp: # 把 t 对象存到文件中
            #    pickle.dump(c, fp)
        savejson(config)

def ResetWordlist():
    wordlistname=get_all_file()
    for item in wordlistname:
        list1=loadfileP(item)
        for it in range(len(list1[0])):
            list1[0][it].wordlist=item
        savefileP(item,list1)


def Speak_init():
    
    
    '''engine.setProperty('rate', 125)     # setting up new voice rate #init=200
    engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1 #init=1
    voices = engine.getProperty('voices')       #getting details of current voice
    #engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
    engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female'''
class SpeakWords_T (threading.Thread):
    def __init__(self, words):
        threading.Thread.__init__(self)
        self.words = words
    def run(self):
        #playsound(yd.down(self.words))
        soundPath=yd.down(str(self.words).replace(' ',''))
        #open(soundPath)
        #os.system(soundPath)
        try:
            #pygame.mixer.init()                           # 初始化
            #track = pygame.mixer.music.load(soundPath)   # 加载音乐文件
            #pygame.mixer.music.play()
            
            
            playsound.playsound(soundPath)
        except Exception as ide:
            #print(f'Error: {ide}')
            print('Info: error in playsound_EN. try playing US.')
            #pygame.mixer.music.stop()
            try:
                yd.setAccent(0)
                soundPath=yd.down(str(self.words).replace(' ',''))
                #pygame.mixer.init()                           # 初始化
                #track = pygame.mixer.music.load(soundPath)   # 加载音乐文件
                #pygame.mixer.music.play()
                playsound.playsound(soundPath)
                #time.sleep(10)
                #pygame.mixer.music.stop()
                yd.setAccent(1)
            except Exception as ide:
                
                #print(f'Error: {ide}')
                print('Info:Cannot Play Sound. Filename:'+self.words)
        
        #由于未知原因，某些特殊音频无法在python中播放，已查明的有EN-individual.mp3
        #Play_mp3.play(soundPath)
            #engine.say(self.words) 
            #engine.runAndWait()
            #engine.stop()
        #except:
        #    print('too quickly')
        


def SpeakWords(words):
    thread1 = SpeakWords_T(words)
    thread1.start()
    #thread1.join()
    """Saving Voice to a file"""
    # On linux make sure that 'espeak' and 'ffmpeg' are installed
    #engine.save_to_file('Hello World', 'test.mp3')
    #engine.runAndWait()	

'''def SpeakWords_T(words):
    engine.say(words)
    engine.runAndWait()
    engine.stop()'''

'''def SpeakWordsOLD(words):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    try:
        speaker.Speak(words)
    except:
        if sys.exc_type is EOFError:
            sys.exit()'''
#forget()
