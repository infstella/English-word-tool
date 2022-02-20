import os
os.chdir('../')
from ALLwindow import *

notebook.add(frame1, text="单词列表")
notebook.add(frame2, text="背单词")
notebook.add(frame3, text="设置")
notebook.pack(padx=10, pady=5, fill=BOTH, expand=True)

root.bind("<Return>", enterevent)
#root.mainloop()

#savefile()



def jiemian1():
    root1=Tk()
    root1.geometry('800x600')
    #bu1=Button(root1,text="第一个窗口",command=lambda:[root1.destroy(),jiemian2()])
    selectableMsg = Text(root1,width=800,height=600,relief='flat',bg='gray94',wrap='word',font=MICROFONT)
    selectableMsg.insert(END,'帮助文件请参阅\'https://docs.qq.com/doc/DRGlYR0JVTWJBcVNl\'(Ctrl+c复制)\n')
    selectableMsg.insert(END,'更多信息可加qq群:596067731\n')
    selectableMsg.configure(state='disabled')
    selectableMsg.pack()
    #Flb1 = Label(root1, text='帮助文件请参阅\'https://docs.qq.com/doc/DRGlYR0JVTWJBcVNl\'',font=font)
    #Flb1.pack()
    root1.mainloop()

def jiemian2():
    root2=Tk()
    root2.geometry('800x600')
    selectableMsg = Text(root2,width=800,height=600,relief='flat',bg='gray94',wrap='word',font=MICROFONT)
    selectableMsg.insert(END,'当前版本:'+LOCAL_SOFTWARE_VERSION+'\n')
    selectableMsg.configure(state='disabled')
    selectableMsg.pack()
    #bu1=Button(root2,text="第二个窗口",command=lambda:[root2.destroy(),jiemian1()])
    #Flb1 = Label(root2, text='',font=font)
    root2.mainloop()

#jiemian1()



#root=Tk()
#root.title('GUI')#标题
#root.geometry('800x600')#窗体大小
#root.resizable(False, False)#固定窗体
def Fhelp():
    #print('p')
    jiemian1()
    
def Fabout():
    #print('p')
    jiemian2()

f = Menu(root)#创建根菜单
root['menu'] = f#顶级菜单关联根窗体

#f1=Menu(f,tearoff=False)#创建子菜单
#f2=Menu(f)

#f1.add_command(label='打开')#子菜单栏
#f1.add_command(label='保存',command=p)
#f2.add_command(label='复制')
#f2.add_command(label='删除')

#f.add_cascade(label='文件',menu=f1)#创建顶级菜单栏，并关联子菜单
#f.add_cascade(label='编辑',menu=f2)
f.add_cascade(label='帮助',command=Fhelp)
f.add_cascade(label='关于',command=Fabout)
SpeakWords('individual')
root.mainloop()