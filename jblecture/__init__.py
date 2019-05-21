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
import zipfile

defaults = {}
defaults['TITLE'] = 'TempTitle'
defaults['HOME_DIR'] = pathlib.Path.home().resolve()
defaults['ORIG_ROOT'] = pathlib.Path('.').resolve()
defaults['ROOT_DIR'] = defaults['ORIG_ROOT'] / 'BuildDir'
defaults['MODULE_ROOT'] = defaults['ORIG_ROOT'] / 'NTNU-Lectures'

defaults['REVEAL_DIR'] = defaults['ROOT_DIR'] / "reveal.js" 
defaults['ASSETS_DIR'] = defaults['REVEAL_DIR'] / "assets"
defaults['IMAGES_DIR'] = defaults['ASSETS_DIR'] / "images"
defaults['VIDEOS_DIR'] = defaults['ASSETS_DIR'] / "videos"
defaults['SOUNDS_DIR'] = defaults['ASSETS_DIR'] / "sounds"

defaults['RENPY_GAME_DIR'] = defaults['ROOT_DIR'] / "renpy" / "game"
defaults['RENPY_ASSETS_DIR'] = defaults['RENPY_GAME_DIR'] / "assets"
defaults['RENPY_IMAGES_DIR'] = defaults['RENPY_ASSETS_DIR'] / "images"
defaults['RENPY_SOUNDS_DIR'] = defaults['RENPY_ASSETS_DIR'] / "sounds"
defaults['RENPY_VIDEOS_DIR'] = defaults['RENPY_ASSETS_DIR'] / "videos"

defaults['GIT_CMD'] = 'git'

defaults['GOOGLE_COLAB'] = False
try:
    from google.colab import files
except ImportError:
    defaults['GOOGLE_COLAB'] = False

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
		<link rel="stylesheet" href="css/theme/{{ REVEAL_THEME }}.css">

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
    <img class="jb-footer-left-img plain" src="{{ cfg['ASSETS']['logo'].__repr_html_b64__() }}" alt="{{cfg['ASSETS']['logo'].name}}" />
</div>
<div class="jb-footer-right">
    <img class="jb-footer-right-img plain" src="{{ cfg['ASSETS']['robbi'].__repr_html_b64__() }}" alt="{{ cfg['ASSETS']['robbi'].name}}" />
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

    with jbcd.JBcd( cfg['ROOT_DIR'] / 'reveal.js' ):
        print("Executing npm install decktape")
        try:
            o = subprocess.check_output("npm install decktape", shell = True)
        except subprocess.CalledProcessError:
            pass
        if ( o ):    
            print( 'npm install decktape:' + o.decode('utf-8') )

    for d in [ cfg['IMAGES_DIR'], cfg['VIDEOS_DIR'], cfg['SOUNDS_DIR'] ]:
        d.mkdir( parents = True, exist_ok=True )
        
    updateGit( cfg, "https://github.com/guichristmann/Lecture-VN.git", "Lecture-VN", "", cfg['ORIG_ROOT'] )

    with jbcd.JBcd( cfg['ROOT_DIR'] ):
        print("Creating renpy directory in " + str( cfg['ROOT_DIR'] ) )
        for d in [ cfg['RENPY_GAME_DIR'], cfg['RENPY_ASSETS_DIR'], cfg['RENPY_IMAGES_DIR'], cfg['RENPY_IMAGES_DIR'] / "slides", 
		  cfg['RENPY_SOUNDS_DIR'], cfg['RENPY_VIDEOS_DIR'], cfg['RENPY_GAME_DIR'] / "tl" ]:
            pathlib.Path(d).mkdir( parents = True, exist_ok = True )
    for f in [ 'characters.rpy', 'gui.rpy', 'options.rpy', 'screens.rpy', 'script.rpy', 'transforms.rpy' ]:
        shutil.copy2( cfg['ORIG_ROOT'] / 'Lecture-VN' / 'Resources' / 'templateProject' / 'game' / f,
                      cfg['ROOT_DIR'] / 'renpy' / 'game')
    shutil.copytree( cfg['ORIG_ROOT'] / 'Lecture-VN' / 'Resources' / 'templateProject' / 'game' / 'gui',
                     cfg['ROOT_DIR'] / 'renpy' / 'game' / 'gui' )
     
    shutil.copy2( cfg['ORIG_ROOT'] / 'NTNU-Lectures' / 'html' / 'ntnuerc.css' , 
        cfg['ROOT_DIR'] / 'reveal.js' / 'css' / 'theme'  )
    shutil.copy2(  cfg['ORIG_ROOT'] / 'NTNU-Lectures' / "images" / "ntnuerc-logo-1.png", 
        cfg['IMAGES_DIR'] / 'robbi.png' )
    shutil.copy2(  cfg['ORIG_ROOT'] / 'NTNU-Lectures' / "images" / "ntnu-ee-logo.png", 
        cfg['IMAGES_DIR']  / 'logo.png')

    cfg['ASSETS'] = {}

    cfg['ASSETS']['robbi'] = jbdata.JBImage( name='robbi', width=162, height=138, localFile= str( cfg['IMAGES_DIR']  / "robbi.png" ) )
    cfg['ASSETS']['logo'] =  jbdata.JBImage( name = 'logo', width=0, height=0, localFile= str( cfg['IMAGES_DIR'] / "logo.png" ) )

    installRenpy()
    
    ratio = 1.0
    cssStr = """
        @page {{
            size: {width}px {height}px;
            margin: 0px;
        }}""".format(width=cfg['PAGE_SIZE'][0], height=cfg['PAGE_SIZE'][1])
    doc = createDocument( cfg )
    cfg['doc'] = doc
    return cfg

def createDocument( cfg ):
    doc = jbdocument.JBDocument( cfg['TITLE'], theme = cfg['REVEAL_THEME'],
        background = cfg['REVEAL_SLIDE_BACKGROUND'],
        footer = cfg['REVEAL_SLIDE_FOOTER'], header=cfg['REVEAL_SLIDE_HEADER'] )
    return doc

def zipDirectory( archive, dir, root = '.' ):
    with jbcd.JBcd(root):
        xroot = dir

        with zipfile.ZipFile( archive, 'w', zipfile.ZIP_DEFLATED, True ) as zf:
            zf.Debug = 3
            for root, dirs, files in os.walk( xroot ):
                #print(root, dirs, files )

                for f in files:
                    zf.write( pathlib.Path( root ).joinpath( f ) )

                for rdir in [ '.git', 'node_modules' ]:
                    if ( rdir in dirs ):
                        dirs.remove( rdir )

        #print('Zipping Files', filesList)

        with zipfile.ZipFile( archive, 'r' ) as zf:
            zf.namelist()

def downloadDir( zFile, dir, root = None  ):        
    zipDirectory(  zFile, dir, root )
    if cfg['GOOGLE_COLAB']:
        files.download( zFile )

def installRenpy():
    os.system("sudo apt install renpy") 

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

# Functions that should be exported
def addJBImage( name, width, height, url=None, data=None, localFile=None ):
    img = jbdata.JBImage( name, width, height, url, data, localFile )
    cfg['ASSETS'][img.name] = img
    return img

def addJBVideo( name, width, height, url=None, data=None, localFile=None ):
    vid = jbdata.JBVideo( name, width, height, url, data, localFile )
    cfg['ASSETS'][vid.name] = vid
    return vid

def addJBData( name, url=None, data=None, localFile=None, suffix=".dat" ):
    dat = jbdata.JBData( name, url, data, localFile, suffix )
    cfg['ASSETS'][dat.name] = dat
    return dat

tableT = """
<table style="text-align: left; width: 100%; font-size:0.4em" border="1" cellpadding="2"
cellspacing="2"; border-color: #aaaaaa>
{0}
<tbody>
{1}
</tbody>
</table>
"""

trT = """
<tr>
{0}
</tr>
"""

tdT = """
<td style="vertical-align: top;">
{0}
</td>
"""

thT = """
<th>
{0}
</th>
"""

def createTable( data, index = None, columns = None, tableT = tableT, thT = thT, tdT = tdT, trT = trT ):
    if columns:
        cdata = """
        <thead>
          <tr>
        """
        for c in columns:
            cdata = cdata + thT.format(c)
        cdata = cdata + """
          </tr>
        </thead>
        """
    else:
        cdata = ""

    bdata = ""
    for i,r in enumerate( data ):
        rdata = ""
        for j,d in enumerate( r ):
            rdata = rdata + tdT.format( d )
        row = trT.format( rdata )
        #print(row)
        bdata = bdata + row
    #/print(bdata)
    table = tableT.format( cdata, bdata )
    return table

def instTemplate( text, vars ):
    prev = ""
    current = text
    while( prev != current ):
        t = Template( current )
        prev = current
        current = t.render( vars )
    return current
