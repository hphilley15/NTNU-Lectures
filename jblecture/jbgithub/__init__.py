from github import Github
import os
import getpass
import pathlib
from ..jbcd import JBcd
import subprocess

cfg = {}

def createEnvironment( mycfg ):
    global cfg
    cfg = mycfg
    cfg['GITHUB'] = None
    return cfg


def readGithubToken():
    passwd = getpass.getpass("Github Token:")    
    return passwd

def login( token ):
    cfg['GITHUB'] = Github( token )

def getRepositories( ):
    repos = None
    if 'GITHUB' in cfg and cfg['GITHUB']:
        repos = cfg['GITHUB'].get_user().get_repos()
    return repos

def findRepoByName( title ):
    repo = None
    if 'GITHUB' in cfg and cfg['GITHUB']:
        repos = getRepositories()
        if repos:
            for r in repos:
                if r.name == title:
                    repo = r
                    break
    return repo


def runCommand( cmd ):
    o = None
    try:
        o = subprocess.check_output( cmd, shell=True)
    except subprocess.CalledProcessError:
        pass
    if ( o ):
        print( "Output " + cmd + ":\n" + o.decode('utf-8') )

def createLocalGit(title, root ):
    p = pathlib.Path( root ) / pathlib.Path( title )

    repo = findRepoByName( title )
    if repo:
        if p.is_dir():                
            with JBcd( p ):
                print("Executing git pull")
                runCommand( cfg['GIT_CMD'] + " pull" )
        else:
            p.mkdir( parents=True, exist_ok= True )
            with JBcd( pathlib.Path( root ) ):
                runCommand( cfg['GIT_CMD'] + " clone " + repo.name + " ." )
    else:
        if p.is_dir():
            pass
        else:
            p.mkdir( parents=True, exist_ok= True )
            dirs = ["css", "js", "assets/images", "assets/videos", "assets/sounds" ]
            for d in dirs:
                x = p / d
                x.mkdir( parents=True, exists_ok=True )
            runCommand( cfg['GIT_CMD'] + " init" )
            with JBcd( p ):
                for d in dirs:
                    runCommand( cfg['GIT_CMD'] + " add " + d )

            # if not p.is_dir():
            #     print("cloning {0} from url {1} root {2}".format( dirname, url, root ), 'git command', cfg['GIT_CMD'])
            #     if ( branch ):
            #         bs = " --branch " + branch
            #     else:
            #         bs = ""
                    
            #     cmd = cfg['GIT_CMD'] + " clone " + bs + " " + url + " " + dirname 
            #     os.system( cmd )
            # else:
            #     print("git directory exists")

            # with JBcd( dirname ):
            #     print("Executing git pull")
            #     o = None
            #     try:
            #         o = subprocess.check_output(cfg['GIT_CMD'] + " pull", shell=True)
            #     except subprocess.CalledProcessError:
            #         pass
            #     if ( o ):
            #         print( 'git pull:' + o.decode('utf-8') )
