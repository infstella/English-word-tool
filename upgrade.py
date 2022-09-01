TotalList=[]
from unit import *
checkinit()
wordlistname=get_all_file()
def upgrade_0(list1):
    list1=[list1,{'version':'v0.1','num_version':1}]
    return list1

def upgrade_1(list1,n):
    list1[1]={'version':'v0.2','num_version':2}
    item=list1[0]
    for it in range(len(item)):
        i=list1[0][it]
        list1[0][it]=Word(i.words,i.chinese,i.create_time,i.forget_time,POS=i.POS,remember_rate=i.remember_rate,wordlist=n)
    return list1

def upgrade_2(list1):
    list1[1]={'version':'v0.2.1','num_version':3}
    item=list1[0]
    for it in range(len(item)):
        i=list1[0][it]
        list1[0][it]=Word(i.words,i.chinese,i.create_time,i.forget_time,POS=i.POS,remember_rate=i.remember_rate,wordlist=i.wordlist,wrong_num=0,tip_num=0)
    return list1

def Up_start():
    for item in wordlistname:
        list1=loadfileP(item)
        '''if list1[1]['num_version']!=1:
            list1=upgrade_0(list1)
            savefileP(item,list1)'''
        if list1[1]['num_version']==1:
            list1=upgrade_1(list1,item)
            savefileP(item,list1)
        elif list1[1]['num_version']==2:
            list1=upgrade_2(list1)
            savefileP(item,list1)
#Up_start()