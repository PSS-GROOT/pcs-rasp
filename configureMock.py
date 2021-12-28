#!/usr/bin/env python
import subprocess,os,sys,enum
instanceQty = 10

class SCRIPT_TYPE(enum.Enum):
    PYTHON = 1
    SHELL = 2

stype = SCRIPT_TYPE.SHELL.value

for i in range(0,instanceQty):
    print(os.getcwd())
    if stype == SCRIPT_TYPE.PYTHON.value :
        subprocess.Popen([sys.executable,f"{os.getcwd()}/mockScript.py",str(i)])
    elif stype == SCRIPT_TYPE.SHELL.value :
        subprocess.Popen(f"{os.getcwd()}/mockScript.sh {i}",shell=True,executable='/bin/bash')
    else :
        print(f"SCRIPT_TYPE invalid. {stype}")

    
