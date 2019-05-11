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
defaults['ROOT_DIR'] = defaults['ORIG_ROOT'] / defaults['TITLE']
defaults['MODULE_ROOT'] = defaults['ORIG_ROOT'] / 'NTNU-Lectures'
defaults['IMAGES_DIR'] = defaults['ROOT_DIR'] / "reveal.js" / "assets" / "images"
defaults['VIDEOS_DIR'] = defaults['ROOT_DIR'] / "reveal.js" / "assets" / "videos"
defaults['SOUNDS_DIR'] = defaults['ROOT_DIR'] / "reveal.js" / "assets" / "sounds"
defaults['GIT_CMD'] = 'git'
defaults['THEME'] = 'ntnuerc'
defaults['INSTALL_DEPENDENCIES'] : True
defaults['REVEAL_PRESENTATION_TEMPLATE'] = """
<!doctype html>
<html>
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">

		<title>{{title}}</title>

		<link rel="stylesheet" href="css/reveal.css">
		<link rel="stylesheet" href="css/theme/{{THEME}}.css">

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

def updateGit( url, dirname, branch,  root ):
        with JBcd( root ):
            p = pathlib.Path( dirname )
            if not p.is_dir():
                print("cloning {0} from url {1} root {2}".format( dirname, url, root ), 'git command', GIT_CMD)
                if ( branch ):
                    bs = " --branch " + branch
                else:
                    bs = ""
                    
                cmd = GIT_CMD + " clone " + bs + " " + url + " " + dirname 
                os.system( cmd )
            else:
                print("git directory exists")

            with JBcd( dirname ):
                print("Executing git pull")
                o = None
                try:
                    o = subprocess.check_output(GIT_CMD + " pull", shell=True)
                except subprocess.CalledProcessError:
                    pass
                if ( o ):
                    print( 'git pull:' + o.decode('utf-8') )

def loadModules( cfg ):
    print('Loading Modules', cfg['MODULE_ROOT'])
    if cfg['MODULE_ROOT'] not in sys.path:
        sys.path.append( cfg['MODULE_ROOT'] )
    print('sys.path', sys.path )    
    from .jbcd import JBcd
    from .jbdata import JBImage, JBVideo
    from .jbslide import JBSlide
    from .jbmagics import JBMagics
    from .jbdocument import JBDocument

def createDocEnvironment( params = {} ):
    cfg = { **defaults, **params }
    
    cfg['ROOT_DIR'].mkdir(parents = True, exist_ok = True )

    node = platform.node()

    for p in [ "weasyprint", "pygments", "youtube-dl", "jinja2" ]:
        try:
            importlib.import_module( p )
        except ImportError:
            print('Using pip to install missing dependency', p)
            os.system("pip" + " install " + p )

    loadModules( cfg )

    updateGit( "https://github.com/hakimel/reveal.js.git", "reveal.js", "", cfg['ROOT_DIR'] )

    with JBcd( cfg['ROOT_DIR'] / 'reveal.js' ):
        print("Executing npm install")
        try:
            o = subprocess.check_output("npm install", shell = True)
        except subprocess.CalledProcessError:
            pass
        if ( o ):    
            print( 'npm install:' + o.decode('utf-8') )

    for d in [ cfg['IMAGES_DIR'], cfg['VIDOES_DIR'], cfg['SOUNDS_DIR'], cfg['DATA_DIR'] ]:
        d.mkdir( parents = True, exist_ok=True )
        
    updateGit( "https://github.com/guichristmann/Lecture-VN.git", "Lecture-VN", "", cfg['ROOT_DIR'] )

    with JBcd(ROOT_DIR):
        print("Creating renpy directory in " + str( cfg['ROOT_DIR'] ) )
        for d in ["renpy", "renpy/game", "renpy/images/Slides", "renpy/assets/images/slides", "renpy/assets/sounds", "renpy/assets/videos", "renpy/gui", "renpy/tl" ]:
            pathlib.Path(d).mkdir( parents = True, exist_ok = True )

    shutil.copy( cfg['ORIG_ROOT'] / 'html' / 'ntnuerc.css' , cfg['ORIG_ROOT'] / 'reveal.js' / 'css' / 'theme'  )

    cfg['IMAGES'] = [
        JBImage( name='robbi', width=162, height=138, localFile= cfg['MODULE_ROOT'] / 'assets' / "images" / "robbi.png" ),
        JBImage( name = 'logo', width=0, height=0, localFile= cfg['MODULE_ROOT'] / "assets" / "images" / "logo.png" )
    ]

    ratio = 1.0
    cssStr = """
        @page {{
            size: {width}px {height}px;
            margin: 0px;
        }}""".format(width=cfg['PAGE_SIZE'][0], height=cfg['PAGE_SIZE'][1])

    doc = JBDocument( cfg['TITLE'], theme = cfg['THEME'], footer = cfg['revealSlideFooter'], header=cfg['revealSlideHeader'] )
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

    cfg = createDocEnvironment()
    magics = JBMagics( ipython, cfg['doc'] )
    doc.user_ns = magics.shell.user_ns
    ipython.register_magics(magics)
    