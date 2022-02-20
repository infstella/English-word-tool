class Word():
    def __init__(self,words,chinese,create_time,forget_time,POS='U',remember_rate=0,wordlist=''):#POS:U=unknow,P=phrase
        self.words=words
        self.create_time=create_time
        self.chinese=chinese
        self.forget_time=forget_time
        self.remember_rate=remember_rate
        self.POS=POS
        self.wordlist=wordlist

    def getwords(self):
        return self.words

    def getcreate_time(self):
        return self.create_time

    def getforget_time(self):
        return self.forget_time

    def getPOS(self):
        return self.POS
    
    def getwordlist(self):
        return self.wordlist

    def setforget_time(self,forget_time):
        self.forget_time=forget_time




'''a=chooseWords(2)
tlearn=a
def show():
    randomnum=random.randint(0,len(tlearn)-1)
    testword=tlearn[randomnum]
    print(testword.chinese,end=' ')
    inp=input()
           

def cac(inp):
    if inp==testword.words:
        tlearn.remove(testword)
        TotalList[ TotalList.index(testword) ]. remember_rate=1
        print('正确:)')
    else:
        print('错误:(，你的答案和正确答案是 ' , inp , tlearn[randomnum].words)'''