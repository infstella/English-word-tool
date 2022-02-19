global TotalList
import random
import upgrade
from tkinter import *
from WordPattern import *
from tkinter import ttk
from unit import *
from tkinter import scrolledtext

start()
upgrade.Up_start()
root=Tk()
root.geometry('1920x1080')
notebook=ttk.Notebook(root)
CACHE_NUM=0
frame1 = Frame(root)
frame2 = Frame(root)
frame3 = Frame(root)
setting=loadjson()

global tlearn
tlearn=[]
global testword
global state,Atype
global state2
global flag_repete
flag_repete=False
Atype=0
randomnum=0
testword=None
state=0
state2=0
showL=['英文','中文','创建时间','上次遗忘时间','记忆率','词性']
wordlistname=[]
wordlistname=get_all_file()


#------------------A-------------------------#


def Arun1(event=None):
    TotalList[0].append(Word(words=Ainp1.get(),chinese=Ainp2.get(),create_time=today_date,forget_time=today_date,POS=Ainp4.get()))
    Av.set('设置成功!')
    Aflashtext()

def Arun2():
    TotalList[0].pop(int(Ainp3.get()))
    Aflashtext()

def Aflashtext():
    for item in tree.get_children():
          tree.delete(item)
    for i in TotalList[0]:          
        tree.insert("", TotalList[0].index(i), text=str(TotalList[0].index(i)), values=(str(i.words), str(i.chinese), str(i.create_time), str(i.forget_time),str(round(i.remember_rate,2)),str(i.POS)))


def Ago(x):
    global TotalList
    TotalList=loadfileP(Acomboxlist.get())
    print('event:选择列表')
    Av4.set('版本:'+TotalList[1]['version'])
    Aflashtext()

def updateTime():
    #v2.set(translate_content_ch(inp1.get()))
    Alb2.after(5000, updateTime)

def Asave():
    Aflashtext()
    savefileP(Acomboxlist.get(),TotalList)
    #with open('wordlist//'+Acomboxlist.get(), 'w+b') as fp:
    #    pickle.dump(TotalList, fp)
        #print(len(TotalList[1]))
    Av.set('保存成功')
    Aflashtext()

def AEdit():
    if Ainp2.get()!='':
        TotalList[0][int(Ainp3.get())].chinese=Ainp2.get()
    if Ainp4.get()!='':
        TotalList[0][int(Ainp3.get())].POS=Ainp4.get()
    Aflashtext()
    Av.set('修改成功')
    
def treeclick(event):
    item = tree.selection() #'I001'、'I002'
    if item:
        txt = int(tree.item(item[0],'text'))
    try:
        Ainp2v.set(TotalList[0][txt].chinese)
        Ainp1v.set(TotalList[0][txt].words)
        Ainp4v.set(TotalList[0][txt].POS)
        Ainp3v.set(txt)
    except UnboundLocalError:
        print('Message:UnboundLocalError in treeclick()')
    
def AFindtext():
    a=Ainp1.get()
    for item in TotalList[0]:
        if item.words==a:
            i=TotalList[0].index(item)
            Ainp2v.set(TotalList[0][i].chinese)
            Ainp1v.set(TotalList[0][i].words)
            Ainp4v.set(TotalList[0][i].POS)
            Ainp3v.set(i)

Av = StringVar()
Av.set("Hello")

Av2 = StringVar()
Av2.set("Hello")

Av3 = StringVar()
Av3.set("文件名:")

Av4 = StringVar()
Av4.set("版本:")

Ainp1v= StringVar()
Ainp2v= StringVar()
Ainp3v= StringVar()
Ainp4v= StringVar()

def frame1_enterevent(event):
    Arun1()
    Ainp1.focus_set()
    Ainp1v.set('')
    Ainp2v.set('')
    Ainp3v.set('')
    Ainp4v.set('')

Alb1 = Label(frame1, textvariable=Av,font=font)
Alb1.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.1)

Alb2 = Label(frame1, textvariable=Av2,font=font)
Alb2.place(relx=0.2, rely=0.3, relwidth=0.2, relheight=0.1)

def Ainp1E(event):
    Ainp2.focus_set()
Ainp1 = Entry(frame1,font=font, textvariable=Ainp1v)#L2
Ainp1.place(relx=0.15, rely=0.2, relwidth=0.3, relheight=0.1)
Ainp1.bind('<Return>',Ainp1E)
def Ainp2E(event):
    Ainp4.focus_set()
Ainp2 = Entry(frame1,font=font, textvariable=Ainp2v)#L3
Ainp2.place(relx=0.55, rely=0.2, relwidth=0.3, relheight=0.1)
Ainp2.bind('<Return>',Ainp2E)

Ainp3 = Entry(frame1,font=font, textvariable=Ainp3v)#L1
Ainp3.place(relx=0.02, rely=0.2, relwidth=0.1, relheight=0.1)
#Ainp1.bind('<Return>',lambda:Ainp1.focus_set())

Ainp4 = Entry(frame1,font=font, textvariable=Ainp4v)#L4
Ainp4.place(relx=0.9, rely=0.2, relwidth=0.05, relheight=0.05)
Ainp4.bind('<Return>',frame1_enterevent)

Alb3 = Label(frame1, textvariable=Av3,font=font)
Alb3.place(relx=0, rely=0.05, relwidth=0.2, relheight=0.05)

Alb4 = Label(frame1, textvariable=Av4,font=MICROFONT)
Alb4.place(relx=0, rely=0.1, relwidth=0.2, relheight=0.05)

Acomvalue=StringVar()#窗体自带的文本，新建一个值
Acomboxlist=ttk.Combobox(frame1,textvariable=Acomvalue) #初始化
Acomboxlist["values"]=(wordlistname)
Acomboxlist.current(wordlistname.index('NewWordsList')) 
Acomboxlist.bind("<<ComboboxSelected>>",Ago) #绑定事件,(下拉列表框被选中时，绑定go()函数)
Acomboxlist.place(relx=0.2, rely=0.05, relwidth=0.2, relheight=0.05)
# 方法-直接调用 run1()
Abtn1 = Button(frame1, text='添加', command=Arun1,font=font)
Abtn1.place(relx=0.25, rely=0.4, relwidth=0.1, relheight=0.1)

Abtn2 = Button(frame1, text='删除', command=Arun2,font=font)
Abtn2.place(relx=0.65, rely=0.4, relwidth=0.1, relheight=0.1)

Abtn3 = Button(frame1, text='保存', command=Asave,font=font)
Abtn3.place(relx=0.65, rely=0.5, relwidth=0.1, relheight=0.1)

Abtn4 = Button(frame1, text='刷新', command=Aflashtext,font=font)
Abtn4.place(relx=0.05, rely=0.4, relwidth=0.1, relheight=0.1)

#Abtn5 = Button(frame1, text='添加列表', command=addlist,font=font)
#Abtn5.place(relx=0, rely=0.5, relwidth=0.1, relheight=0.05)

#Abtn6 = Button(frame1, text='移除列表', command=poplist,font=font)#L1 input
#Abtn6.place(relx=0.1, rely=0.5, relwidth=0.1, relheight=0.05)

Abtn7 = Button(frame1, text='修改', command=AEdit,font=font)
Abtn7.place(relx=0.25, rely=0.5, relwidth=0.1, relheight=0.1)

Abtn8 = Button(frame1, text='查找', command=AFindtext,font=font)
Abtn8.place(relx=0.05, rely=0.5, relwidth=0.1, relheight=0.1)

# 在窗体垂直自上而下位置60%处起，布局相对窗体高度40%高的文本框


Ainp1.focus_set()

#sc1=ttk.Scrollbar(frame1)
#sc1.place(relx=0, rely=0.6, relwidth=1, relheight=0.35)

treestyle = ttk.Style()
treestyle.configure("Treeview", font=FONT)
treestyle.configure("Treeview.Heading", font=HEADFONT)
treestyle.configure('Treeview', rowheight=30)
#style_head.configure("Treeview.Item", font=font)

tree = ttk.Treeview(frame1)
tree.place(relx=0, rely=0.6, relwidth=1, relheight=0.35)
tree["columns"] = (showL[0], showL[1], showL[2], showL[3], showL[4], showL[5]) 

tree.bind('<ButtonRelease-1>',treeclick)

for i in range(6):
    tree.column(showL[i], width=100)
    tree.heading(showL[i], text=showL[i])        # #设置显示的表头名



#----------------S------------------#




Sv2 = StringVar()
Sv2.set("背单词计划:")
Sv3 = StringVar()
Sv3.set("Hello")
Siv1 = StringVar()
Siv1.set(setting['Old'])
Siv2 = StringVar()
Siv2.set(setting['New'])
Siv3 = StringVar()
Siv3.set(setting['wordlist'])


def cw():
    global tlearn
    a=[]
    d=setting['wordlist']
    d=list(d.split(','))
    if setting['wordlist']=='':
        return
    for i in d:
        c=loadfileP(i)
        a=a+c[0]
    tlearn=chooseWords(int(setting['Old']),CHOOSE_OLD,a) 
    tlearn+=chooseWords(int(setting['New']),CHOOSE_NEW,a)
    
    print()

def Srun1():
    global setting
    setting['Old']=Sinp1.get()
    setting['New']=Sinp2.get()
    setting['wordlist']=Sinp3.get()
    savejson(setting)
    cw()
    print()

def Sgo(x):
    print()
    Siv3.set(Siv3.get()+','+Scomboxlist.get())


Scomvalue=StringVar()#窗体自带的文本，新建一个值
Scomboxlist=ttk.Combobox(frame3,textvariable=Scomvalue) #初始化
Scomboxlist["values"]=(wordlistname)
Scomboxlist.current(0) #选择第一个
Scomboxlist.bind("<<ComboboxSelected>>",Sgo) #绑定事件,(下拉列表框被选中时，绑定go()函数)
Scomboxlist.place(relx=0.2, rely=0.05, relwidth=0.2, relheight=0.05)

Slb2 = Label(frame3, textvariable=Sv2,font=font)
Slb2.place(relx=0, rely=0.15, relwidth=0.2, relheight=0.05)

Sinp1 = Entry(frame3,font=font,textvariable=Siv1)
Sinp1.place(relx=0.2, rely=0.15, relwidth=0.05, relheight=0.05)

Sinp2 = Entry(frame3,font=font,textvariable=Siv2)
Sinp2.place(relx=0.26, rely=0.15, relwidth=0.05, relheight=0.05)

Sinp3 = Entry(frame3,font=font,textvariable=Siv3)
Sinp3.place(relx=0.35, rely=0.15, relwidth=0.2, relheight=0.05)

Sbtn1 = Button(frame3, text='确认', command=Srun1,font=font)
Sbtn1.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

#--------------------R-----------------#

Alist=[]

def start():
    global Alist
    
    
    Alist=a
def Afind(x):
    d=setting['wordlist']
    d=list(d.split(','))
    for i in d:
        T=loadfileP(i)
        #with open('wordlist//'+i, 'rb') as fp:  # 把 t 对象从文件中读出来，并赋值给 t2
        #    T = pickle.load(fp)
        for ii in T[0]:
            if ii.words==x.words:
                T[0][T[0].index(ii)]=x
        savefileP(i,T)
        #with open('wordlist//'+i, 'w+b') as fp: # 把 t 对象存到文件中
        #    pickle.dump(T, fp)
            

#start()
cw()
def Rrun1():
    global testword,state
    global flag_repete
    state=1
    if len(tlearn)==0:
        Rv3.set('今天背完啦')
    else:
        a = Rinp1.get()
        #print(testword.words)
        
        if a==testword.words:
            if flag_repete:
                flag_repete=False
                Rv.set('正确重复:）')  
            else:
                tlearn.remove(testword)
                testword.remember_rate=1
                Afind(testword)
                Rv.set('正确:）')  
        else:
            Rv.set('错误:（，正确答案是 '+str(testword.words))
            testword.forget_time=today_date
            testword. remember_rate=0
            Afind(testword)
            SpeakWords(testword.words)
            flag_repete=True
    

def Rrun2():
    global testword,state
    state=0
    global flag_repete
    if len(tlearn)==0:
        Rv3.set('今天背完啦')
    else:
        if flag_repete:
            testword=testword
        else:
            randomnum=random.randint(0,len(tlearn)-1)
            testword=tlearn[randomnum]
        #print(testword.words)
        Rinp1.delete(0, END)  # 清空输入
        Rv.set(testword.chinese+'     '+testword.POS)
        Rv2.set('上次记录日期:'+str(testword.forget_time)+' 记忆率:'+str(round(testword.remember_rate,2))+' 加入时间:'+str(testword.create_time))
        Rv3.set("剩余单词数:"+str(len(tlearn)))
        
def Rrun3():
    tlearn.remove(testword)
    testword.remember_rate=1
    Afind(testword)
    Rv.set('OK')
    
def Rrun4():
    SpeakWords(testword.words)


    
def enterevent(event):
    card_num=notebook.index(notebook.select())
    global testword,state,state2
    if card_num==0:
        a=0
    elif card_num==1:
        if state==0:
            Rrun1()
        elif state==1:
            Rrun2()

Rv = StringVar()
Rv.set("Hello")
Rv2 = StringVar()
Rv2.set("Hello")
Rv3 = StringVar()
Rv3.set("Hello")

Rlb1 = Label(frame2, textvariable=Rv,font=font)
Rlb1.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.1)

Rlb2 = Label(frame2, textvariable=Rv2,font=font)
Rlb2.place(relx=0.1, rely=0.8, relwidth=0.8, relheight=0.1)

Rlb3 = Label(frame2, textvariable=Rv3,font=font)
Rlb3.place(relx=0.1, rely=0.6, relwidth=0.8, relheight=0.1)

Rinp1 = Entry(frame2,font=font)
Rinp1.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.1)

Rbtn1 = Button(frame2, text='确认', command=Rrun1,font=font)
Rbtn1.place(relx=0.1, rely=0.4, relwidth=0.3, relheight=0.1)

Rbtn2 = Button(frame2, text='下一个', command=Rrun2,font=font)
Rbtn2.place(relx=0.6, rely=0.4, relwidth=0.3, relheight=0.1)

Rbtn3 = Button(frame2, text='So Easy', command=Rrun3,font=font)
Rbtn3.place(relx=0.6, rely=0.5, relwidth=0.3, relheight=0.1)

Rbtn4 = Button(frame2, text='播放读音', command=Rrun4,font=font)
Rbtn4.place(relx=0.8, rely=0.2, relwidth=0.1, relheight=0.1)



#----------------------------#
Rrun2()
Aflashtext()
updateTime()
#savefile() 
print()