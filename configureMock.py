#!/usr/bin/env python
import subprocess,os,sys,enum
import platform
instanceQty = 1

class SCRIPT_TYPE(enum.Enum):
    PYTHON = 1
    SHELL = 2

stype = SCRIPT_TYPE.SHELL.value

for i in range(0,instanceQty):
    print(os.getcwd())
    if stype == SCRIPT_TYPE.PYTHON.value :

        path = os.path.join(os.getcwd(),"mockScript.py")
        subprocess.Popen([sys.executable,path,str(i)])
    elif stype == SCRIPT_TYPE.SHELL.value :
        path = os.path.join(os.getcwd(),f"mockScript.sh {i}")
        print(path,'shell path')
        if platform.system() != "Windows" :
            subprocess.Popen(path,shell=True,executable='/bin/bash')
        else :
            proc = subprocess.Popen(path,shell=True)
            print("Processes id to kill",proc.pid)
    else :
        print(f"SCRIPT_TYPE invalid. {stype}")

    
