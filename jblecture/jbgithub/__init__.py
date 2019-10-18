from github import Github
import os
import getpass

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

def getRositories( ):
    repos = []
    if 'GITHUB' in cfg and cfg['GITHUB']:
        for repo in cfg['GITHUB'].get_user().get_repos():
            repos.append( repo )
    return repos
