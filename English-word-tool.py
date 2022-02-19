import os
print(os.path.abspath(__file__))

os.chdir( os.path.dirname(os.path.abspath(__file__))+'\\mainwindow' )
os.system('mainwindow.exe')