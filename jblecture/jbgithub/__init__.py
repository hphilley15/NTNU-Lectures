from github import Github
import os
import getpass
import pathlib
from ..jbcd import JBcd
import subprocess
import shutil

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
    g = Github( token )
    cfg['GITHUB'] = g
    return g

def getRepositories( ):
    repos = None
    if 'GITHUB' not in cfg or cfg['GITHUB'] is None:
        login( readGithubToken() )
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
    print( "Running command " + cmd )
    o = None
    try:
        o = subprocess.check_output( cmd, shell=True)
    except subprocess.CalledProcessError:
        pass
    if ( o ):
        print( "Output " + cmd + ":\n" + o.decode('utf-8') )

def copyAndAdd( srcPath, destPath ):
    src = str( srcPath )
    dest = str( destPath )
    shutil.copy2( src, dest )
    runCommand( cfg['GIT_CMD'] + " add " + str( dest ) )

def createLocalGit(title, root ):
    p = pathlib.Path( root ) / pathlib.Path( title )
    cfg['GITHUB_DIR'] = p

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
        if not p.is_dir():
            p.mkdir( parents=True, exist_ok= True )
            dirs = ["css", "js", "assets/images", "assets/videos", "assets/sounds" ]
            for d in dirs:
                x = p / d
                x.mkdir( parents=True, exist_ok=True )
            runCommand( cfg['GIT_CMD'] + " init" )

        copyAndAdd( cfg['ORIG_ROOT'] / 'NTNU-Lectures' / 'html' / 'ntnuerc.css' , 
            p / "css" / 'ntnuerc.css'  )
        copyAndAdd( cfg['ORIG_ROOT'] / 'NTNU-Lectures' / 'html' / 'fira.css' , 
            p / "css" / 'fira.css'  )
        copyAndAdd(  cfg['ORIG_ROOT'] / 'NTNU-Lectures' / "images" / "ntnuerc-logo-1.png", 
             p / "assets" / "images" / 'robbi.png' )
        copyAndAdd(  cfg['ORIG_ROOT'] / 'NTNU-Lectures' / "images" / "ntnu-ee-logo.png", 
            p / "assets" / "images" / 'logo.png')
        copyAndAdd(  cfg['ORIG_ROOT'] / 'NTNU-Lectures' / "images" / "FIRA-logo-1.png", 
            p / "assets" / "images" / 'FIRA-logo-1.png')
        copyAndAdd(  cfg['ORIG_ROOT'] / 'NTNU-Lectures' / "images" / "pairLogo.png", 
            p / "assets" / "images" / 'pairLogo.png')
        
        # Copy html, js, and css artefacts
        copyAndAdd(  cfg['ORIG_ROOT'] / 'NTNU-Lectures' / "html" / "ntnu.js", 
            p / "js" / 'ntnu.js')

        for aname in cfg['ASSETS']:
            a = assets[ aname ]
            rpath = pathlib.Path(a.localFile + "." + a.suffix).relative_to( cfg['REVEAL_DIR'] )
            copyAndAdd( str(a.localFile) + "." + a.suffix, 
                        p /  rpath )
            
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
