import subprocess
import pathlib
import os
import wordwrap

try:
    GIT_CMD
except NameError:
    GIT_CMD = 'git'
    
class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = pathlib.Path(newPath).expanduser().resolve()

    def __enter__(self):
        self.savedPath = pathlib.Path.cwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def updateGit( url, dirname, branch,  root ):
        with cd( root ):
            p = pathlib.Path( dirname )
            if ( branch ):
                bs = " --branch " + branch
            else:
                bs = ""
            if not p.is_dir():
                print("cloning {0} from url {1} root {2}".format( dirname, url, root ), 'git command', GIT_CMD)
                    
                cmd = GIT_CMD + " clone " + bs + " " + url + " " + dirname 
                os.system( cmd )
            else:
                print("git directory exists")

            with cd( dirname ):
                print("Executing git pull")
                o = None
                try:
                    o = subprocess.check_output(GIT_CMD + " pull", shell=True)
                except subprocess.CalledProcessError:
                    pass
                if ( o ):
                    print( 'git pull:' + o.decode('utf-8') )

updateGit('https://github.com/cvroberto21/NTNU-Lectures.git', 'NTNU-Lectures', 'mg', '.')

import sys
import pathlib

d = str( pathlib.Path( pathlib.Path('.') / 'NTNU-Lectures' ).resolve() )
if d not in sys.path:    
    sys.path.append(  d )
print('System Path', sys.path)

import platform
import jblecture
from importlib import reload 

jblecture = reload(jblecture)
node = platform.node()

if node == 'NTNU-ERC':
    GIT_CMD = 'D:\PortableApps\GitPortable\bin\git.exe'
else:
    GIT_CMD = 'git'

# %reload_ext jblecture
import jblecture
jblecture.load_ipython_extension( get_ipython() )

from jblecture import addJBImage, addJBVideo, addJBData, createTable, instTemplate, aprint
from jblecture import cfg
from jblecture import downloadDir
from jblecture import 

doc = cfg['doc']
