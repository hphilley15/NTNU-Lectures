# -*- coding: utf-8 -*-
"""
"""

import pathlib
import os
import platform
import subprocess
import glob
import shutil
import importlib
import sys

defaults = {}
defaults['TITLE'] = 'TempTitle'
defaults['HOME_DIR'] = pathlib.Path.home().resolve()
defaults['ORIG_ROOT'] = pathlib.Path('.').resolve()
defaults['ROOT_DIR'] = defaults['ORIG_ROOT'] / 'BuildDir'
defaults['MODULE_ROOT'] = defaults['ORIG_ROOT'] / 'NTNU-Lectures'
defaults['IMAGES_DIR'] = defaults['ROOT_DIR'] / "reveal.js" / "assets" / "images"
defaults['VIDEOS_DIR'] = defaults['ROOT_DIR'] / "reveal.js" / "assets" / "videos"
defaults['SOUNDS_DIR'] = defaults['ROOT_DIR'] / "reveal.js" / "assets" / "sounds"
defaults['GIT_CMD'] = 'git'


# Reveal.js Parameters
defaults['REVEAL_THEME'] = 'ntnuerc'

defaults['REVEAL_PRESENTATION_TEMPLATE'] = """
<!doctype html>
<html>
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">

		<title>{{title}}</title>

		<link rel="stylesheet" href="css/reveal.css">
		<link rel="stylesheet" href="css/theme/{{ cfg['REVEAL_THEME'] }}.css">

		<!-- Theme used for syntax highlighting of code -->
		<link rel="stylesheet" href="lib/css/zenburn.css">

		<!-- Printing and PDF exports -->
		<script>
			var link = document.createElement( 'link' );
			link.rel = 'stylesheet';
			link.type = 'text/css';
			link.href = window.location.search.match( /print-pdf/gi ) ? 'css/print/pdf.css' : 'css/print/paper.css';
			document.getElementsByTagName( 'head' )[0].appendChild( link );
		</script>
	</head>
	<body>
		<div class="reveal">
        <div class="slides">
            {{slides}}
        </div>
		</div>

		<script src="lib/js/head.min.js"></script>
		<script src="js/reveal.js"></script>

		<script>
			// More info about config & dependencies:
			// - https://github.com/hakimel/reveal.js#configuration
			// - https://github.com/hakimel/reveal.js#dependencies
			Reveal.initialize({
				dependencies: [
					{ src: 'plugin/markdown/marked.js' },
					{ src: 'plugin/markdown/markdown.js' },
					{ src: 'plugin/notes/notes.js', async: true },
					{ src: 'plugin/highlight/highlight.js', async: true, callback: function() { hljs.initHighlightingOnLoad(); } }
				]
			});
		</script>
	</body>
</html>
"""
defaults['REVEAL_SLIDE_TEMPLATE'] = """
<section id="{{id}}">

{{slideHTML}}

<aside class="notes">
{{slideNote}}
</aside>

{{slideChildren}}

</section>
"""

defaults['REVEAL_SLIDE_FOOTER'] = """
<div class="jb-footer-left">
    <img class="jb-footer-left-img plain" src="{{ cfg['ASSETS']['logo'].url }}" alt="{{cfg['ASSETS']['logo'].name}}" />
</div>
<div class="jb-footer-right">
    <img class="jb-footer-right-img plain" src="{{ cfg['ASSETS']['robbi'].url }}" alt="{{cfg['ASSETS']['robbi'].name}}" />
</div>
"""

defaults['REVEAL_SLIDE_HEADER'] = """
"""

defaults['REVEAL_SLIDE_BACKGROUND'] = """
"""

# RENPY Parameters
defaults['RenpyInitTemplate'] = """
define jb = Character("Prof. Jacky Baltes", color="#06799f", callback=speaker("jb"))
define gc = Character("Student G.C.", color="#069f67", callback=speaker("gc"))
define msG = Character("Student G.", color="#069f67", callback=speaker("msG"))

label start:
    show jb neutral at center with dissolve
    
    # Prof. Jacky's Introduction
    jb "Hello! I am Prof. Jacky Baltes."
    
    show jb neutral at center:
        linear 2.0 left
        
    jb "This project describes {{title}}."

    
    jump {{startId}}
"""

defaults['RenpyScriptTemplate'] = """
# Slide {{id}}
label {{label}}:
    scene bg {{id}} with {{transition}}
{{renpy}}
    jump {{right}}
"""

defaults['RenpyTransition'] = "fade"
defaults['RenpyInitLabel'] =  ".init"
defaults['PAGE_SIZE'] = [ int(1280), int (720) ]

def updateGit( cfg, url, dirname, branch,  root ):
        with jbcd.JBcd( root ):
            p = pathlib.Path( dirname )
            if not p.is_dir():
                print("cloning {0} from url {1} root {2}".format( dirname, url, root ), 'git command', cfg['GIT_CMD'])
                if ( branch ):
                    bs = " --branch " + branch
                else:
                    bs = ""
                    
                cmd = cfg['GIT_CMD'] + " clone " + bs + " " + url + " " + dirname 
                os.system( cmd )
            else:
                print("git directory exists")

            with jbcd.JBcd( dirname ):
                print("Executing git pull")
                o = None
                try:
                    o = subprocess.check_output(cfg['GIT_CMD'] + " pull", shell=True)
                except subprocess.CalledProcessError:
                    pass
                if ( o ):
                    print( 'git pull:' + o.decode('utf-8') )

def loadModules( cfg ):
    print('Loading Modules', cfg['MODULE_ROOT'])
    if cfg['MODULE_ROOT'] not in sys.path:
        sys.path.append( str( cfg['MODULE_ROOT']  ) )
    print('sys.path', sys.path )    

    from .jbcd import JBcd

    from .jbdata import createEnvironment, JBImage, JBVideo
    cfg = jbdata.createEnvironment( cfg )

    from .jbslide import createEnvironment, JBSlide
    cfg = jbslide.createEnvironment( cfg )

    from .jbmagics import createEnvironment, JBMagics
    cfg = jbmagics.createEnvironment( cfg )

    from .jbdocument import createEnvironment, JBDocument
    cfg = jbdocument.createEnvironment( cfg )

    print('Loading of modules finished')
    return cfg

def createEnvironment( params = {} ):
    cfg = { **defaults, **params }
    print('Title', cfg['TITLE'] )
    cfg['ROOT_DIR'].mkdir(parents = True, exist_ok = True )

    node = platform.node()

    for p in [ "weasyprint", "pygments", "youtube-dl", "jinja2" ]:
        try:
            importlib.import_module( p )
        except ImportError:
            print('Using pip to install missing dependency', p)
            os.system("pip" + " install " + p )

    cfg = loadModules( cfg )

    updateGit( cfg, "https://github.com/hakimel/reveal.js.git", "reveal.js", "", cfg['ROOT_DIR'] )

    with jbcd.JBcd( cfg['ROOT_DIR'] / 'reveal.js' ):
        print("Executing npm install")
        try:
            o = subprocess.check_output("npm install", shell = True)
        except subprocess.CalledProcessError:
            pass
        if ( o ):    
            print( 'npm install:' + o.decode('utf-8') )

    for d in [ cfg['IMAGES_DIR'], cfg['VIDEOS_DIR'], cfg['SOUNDS_DIR'] ]:
        d.mkdir( parents = True, exist_ok=True )
        
    updateGit( cfg, "https://github.com/guichristmann/Lecture-VN.git", "Lecture-VN", "", cfg['ROOT_DIR'] )

    with jbcd.JBcd( cfg['ROOT_DIR'] ):
        print("Creating renpy directory in " + str( cfg['ROOT_DIR'] ) )
        for d in ["renpy", "renpy/game", "renpy/images/Slides", "renpy/assets/images/slides", "renpy/assets/sounds", "renpy/assets/videos", "renpy/gui", "renpy/tl" ]:
            pathlib.Path(d).mkdir( parents = True, exist_ok = True )

    shutil.copy2( cfg['ORIG_ROOT'] / 'NTNU-Lectures' / 'html' / 'ntnuerc.css' , 
        cfg['ROOT_DIR'] / 'reveal.js' / 'css' / 'theme'  )
    shutil.copy2(  cfg['ORIG_ROOT'] / 'NTNU-Lectures' / "images" / "ntnuerc-logo-1.png", 
        cfg['IMAGES_DIR'] / 'robbi.png' )
    shutil.copy2(  cfg['ORIG_ROOT'] / 'NTNU-Lectures' / "images" / "ntnu-ee-logo.png", 
        cfg['IMAGES_DIR']  / 'logo.png')

    cfg['ASSETS'] = {}

    cfg['ASSETS']['robbi'] = jbdata.JBImage( name='robbi', width=162, height=138, localFile= str( cfg['IMAGES_DIR']  / "robbi.png" ) )
    cfg['ASSETS']['logo'] =  jbdata.JBImage( name = 'logo', width=0, height=0, localFile= str( cfg['IMAGES_DIR'] / "logo.png" ) )

    ratio = 1.0
    cssStr = """
        @page {{
            size: {width}px {height}px;
            margin: 0px;
        }}""".format(width=cfg['PAGE_SIZE'][0], height=cfg['PAGE_SIZE'][1])

    doc = jbdocument.JBDocument( cfg['TITLE'], theme = cfg['REVEAL_THEME'], 
        background = cfg['REVEAL_SLIDE_BACKGROUND'],
        footer = cfg['REVEAL_SLIDE_FOOTER'], header=cfg['REVEAL_SLIDE_HEADER'] )
    cfg['doc'] = doc

    return cfg

def load_ipython_extension(ipython):
    """
    Any module file that define a function named `load_ipython_extension`
    can be loaded via `%load_ext module.path` or be configured to be
    autoloaded by IPython at startup time.
    """
    # This class must then be registered with a manually created instance,
    # since its constructor has different arguments from the default:

    global cfg
    cfg = createEnvironment( {} )
    magics = jbmagics.JBMagics( ipython, cfg['doc'] )
    cfg['doc'].user_ns = magics.shell.user_ns
    ipython.register_magics(magics)
    