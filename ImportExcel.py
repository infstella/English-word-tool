
import xlwings as xw
import time,os
os.chdir('EwtSettings')
from WordPattern import *
from unit import *
import Youdao_Translate
yt=Youdao_Translate.YoudaoTranslate()
MAXNUM=10000
NONE=0
FILLPOS=1
FILLALL=2
class ImportXlsx():
    def __init__(self,translateMode=NONE):   
        open('ImportWordsList.wl','w')
        self.TotalList=[[],{'version':LOCAL_SOFTWARE_VERSION,'num_version':LOCAL_NUM_VERSION}]
        self.app=xw.App(visible=True,add_book=False)
        self.start_open_time=time.time()
        self.wb=self.app.books.open('导入单词.xlsx')
        self.sht = self.wb.sheets[0]
        t1=time.time()
        self.translateMode=translateMode
        print(f'打开工作薄所需要的时间{t1-self.start_open_time}')  
        
        lineA=self.getWordsNum(l='A')
        for i in range(lineA):
            eng=self.sht.range('A'+str(i+2)).value
            if self.translateMode==FILLALL:
                ca=yt.foOutput(eng)
                chi=ca[0]
                pos=ca[1]
            elif self.translateMode==FILLPOS:
                chi=self.sht.range('B'+str(i+2)).value
                ca=yt.foOutput(eng)
                pos=ca[1]
            elif self.translateMode==NONE:
                chi=self.sht.range('B'+str(i+2)).value
            self.addWords(eng,chi,pos)
            
        savefileP('ImportWordsList',self.TotalList)

    def getWordsNum(self,l='A'):
        for i in range(MAXNUM):
            if self.sht.range(l+str(i+1)).value==None:
                return i-1

    def addWords(self,eng,chi,pos):
        self.TotalList[0].append(Word(words=eng,chinese=chi,create_time=today_date,forget_time=today_date,wordlist='ImportWordsList',POS=pos))
        
    def __del__(self):
        self.wb.close()
        self.app.quit()
ImportXlsx(translateMode=FILLPOS)

#重命名单词表时赋值给单词