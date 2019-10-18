from github import Github
import os

cfg = {}

def createEnvironment( mycfg, token ):
    global cfg
    cfg = mycfg
    if 'GITHUB_TOKEN' in os.environ:
        cfg['GITHUB'] = Github( os.environ('GITHUB_TOKEN') )
    else:
        cfg['GITHUB'] = None
    return cfg

def getRositories( ):
    repos = []
    if 'GITHUB' in cfg and cfg['GITHUB']:
        for repo in cfg['GITHUB'].get_user().get_repos():
            repos.append( repo )
    return repos
