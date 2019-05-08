# -*- coding: utf-8 -*-
"""Computer Vision - Optical Flow

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1m6k3WbxKtr5M-wvNvfWNSo6lxGJiOgA4
"""

import __main__
import pathlib

try:
    GIT_CMD = __main__.GIT_CMD
except NameError:
    GIT_CMD = 'git'

try:
    ROOT_DIR = __main__.ROOT_DIR
except NameError:
    ROOT_DIR - pathlib.Path('.')

HOME_DIR = pathlib.Path.home().resolve()
ORIG_ROOT = pathlib.Path( '.' ).resolve() 

ROOT_DIR.mkdir(parents = True, exist_ok = True )

IMAGES_DIR = ROOT_DIR / "reveal.js" / "assets" / "images" 
VIDEOS_DIR = ROOT_DIR / "reveal.js" / "assets" / "videos" 
SOUND_DIR = ROOT_DIR / "reveal.js" / "assets" / "sounds" 
DATA_DIR = ROOT_DIR / "reveal.js" / "assets" / "data"

import platform

node = platform.node()

def getDependencies():
    return [ "weasyprint", "pygments", "youtube-dl", "jinja2" ]

import subprocess
import pathlib
import os
from .cd import cd

def updateGit( url, dirname, root ):
        with cd( root ):
            p = pathlib.Path( dirname )
            if not p.is_dir():
                print("cloning {0} from url {1} root {2}".format( dirname, url, root ), 'git command', GIT_CMD)
                os.system( GIT_CMD + " clone " + url )
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
            
import subprocess
import pathlib
import os
from .cd import cd

updateGit( "https://github.com/hakimel/reveal.js.git", "reveal.js", ROOT_DIR )

with cd( ROOT_DIR / 'reveal.js' ):
    print("Executing npm install")
    try:
        o = subprocess.check_output("npm install", shell = True)
    except subprocess.CalledProcessError:
        pass
    if ( o ):    
        print( 'npm install:' + o.decode('utf-8') )

with cd( ROOT_DIR ):
    pathlib.Path("reveal.js/assets/images").mkdir( parents = True, exist_ok=True )
    pathlib.Path("reveal.js/assets/videos").mkdir( parents = True, exist_ok=True )

updateGit( "https://github.com/guichristmann/Lecture-VN.git", "Lecture-VN", ROOT_DIR )

import pathlib

with cd(ROOT_DIR):
    print("Creating renpy directory in " + str( ROOT_DIR ) )
    for d in ["renpy", "renpy/game", "renpy/images/Slides", "renpy/assets/images/slides", "renpy/assets/sounds", "renpy/assets/videos", "renpy/gui", "renpy/tl" ]:
        pathlib.Path(d).mkdir( parents = True, exist_ok = True )

ntnuRevealTheme="""
/**
 * NTNU ERC theme for reveal.js
 * Author: jacky.baltes <jacky.baltes@gmail.com>
 *
 * Designed to be used with highlight.js theme
 * "monokai_sublime.css" available from
 * https://github.com/isagalaev/highlight.js/
 *
 * For other themes, change $codeBackground accordingly.
 *
 */
 
@import url(https://fonts.googleapis.com/css?family=Ubuntu:300,700,300italic,700italic);
/*********************************************
 * GLOBAL STYLES
 *********************************************/
body {
  background: #522;
  background-color: #522; }

.reveal {
  font-family: Ubuntu, "sans-serif";
  font-size: 40px;
  font-weight: normal;
  color: #eee; }

::selection {
  color: #fff;
  background: #a23;
  text-shadow: none; }

::-moz-selection {
  color: #fff;
  background: #a23;
  text-shadow: none; }

.reveal .slides section,
.reveal .slides section > section {
  line-height: 1.3;
  font-weight: inherit; }

/*********************************************
 * HEADERS
 *********************************************/
.reveal h1,
.reveal h2,
.reveal h3,
.reveal h4,
.reveal h5,
.reveal h6 {
  margin: 0 0 20px 0;
  color: #eee;
  font-family: Ubuntu, "sans-serif";
  font-weight: normal;
  line-height: 1.0;
  letter-spacing: normal;
  text-transform: uppercase;
  text-shadow: 2px 2px 2px #222;
  word-wrap: break-word;
  text-align: center; }

.reveal h1 {
  font-size: 1.80em; }

.reveal h2 {
  font-size: 1.50em; }

.reveal h3 {
  font-size: 1.25em; }

.reveal h4 {
  font-size: 1em; }

.reveal h1 {
  text-shadow: 0 1px 0 #ccc, 0 2px 0 #c9c9c9, 0 3px 0 #bbb, 0 4px 0 #b9b9b9, 0 5px 0 #aaa, 0 6px 1px rgba(0, 0, 0, 0.1), 0 0 5px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.3), 0 3px 5px rgba(0, 0, 0, 0.2), 0 5px 10px rgba(0, 0, 0, 0.25), 0 20px 20px rgba(0, 0, 0, 0.15); }

/*********************************************
 * OTHER
 *********************************************/
.reveal p {
  margin: 20px 0;
  line-height: 1.3; }

/* Ensure certain elements are never larger than the slide itself */
.reveal img,
.reveal video,
.reveal iframe {
  max-width: 95%;
  max-height: 95%; }

.reveal strong,
.reveal b {
  font-weight: bold; }

.reveal em {
  font-style: italic; }

.reveal ol,
.reveal dl,
.reveal ul {
  display: inline-block;
  text-align: left;
  margin: 0 0 0 1em; }

.reveal ol {
  list-style-type: decimal; }

.reveal ul {
  list-style-type: disc; }

.reveal ul ul {
  list-style-type: square; }

.reveal ul ul ul {
  list-style-type: circle; }

.reveal ul ul,
.reveal ul ol,
.reveal ol ol,
.reveal ol ul {
  display: block;
  margin-left: 40px; }

.reveal dt {
  font-weight: bold; }

.reveal dd {
  margin-left: 40px; }

.reveal blockquote {
  display: block;
  position: relative;
  width: 70%;
  margin: 20px auto;
  padding: 5px;
  font-style: italic;
  background: rgba(255, 255, 255, 0.05);
  box-shadow: 0px 0px 2px rgba(0, 0, 0, 0.2); }

.reveal blockquote p:first-child,
.reveal blockquote p:last-child {
  display: inline-block; }

.reveal q {
  font-style: italic; }

.reveal pre {
  display: block;
  position: relative;
  width: 90%;
  margin: 20px auto;
  text-align: left;
  font-size: 0.55em;
  font-family: monospace;
  line-height: 1.2em;
  word-wrap: break-word;
  box-shadow: 0px 0px 6px rgba(0, 0, 0, 0.3); }

.reveal code {
  font-family: monospace;
  text-transform: none; }

.reveal pre code {
  display: block;
  padding: 5px;
  overflow: auto;
  max-height: 400px;
  word-wrap: normal; }

.reveal table {
  margin: auto;
  border-collapse: collapse;
  border-spacing: 0; }

.reveal table th {
  font-weight: bold; }

.reveal table th,
.reveal table td {
  text-align: left;
  padding: 0.2em 0.5em 0.2em 0.5em;
  border-bottom: 1px solid; }

.reveal table th[align="center"],
.reveal table td[align="center"] {
  text-align: center; }

.reveal table th[align="right"],
.reveal table td[align="right"] {
  text-align: right; }

.reveal table tbody tr:last-child th,
.reveal table tbody tr:last-child td {
  border-bottom: none; }

.reveal sup {
  vertical-align: super;
  font-size: smaller; }

.reveal sub {
  vertical-align: sub;
  font-size: smaller; }

.reveal small {
  display: inline-block;
  font-size: 0.6em;
  line-height: 1.2em;
  vertical-align: top; }

.reveal small * {
  vertical-align: top; }

/*********************************************
 * LINKS
 *********************************************/
.reveal a {
  color: #a66;
  text-decoration: none;
  -webkit-transition: color .15s ease;
  -moz-transition: color .15s ease;
  transition: color .15s ease; }

.reveal a:hover {
  color: #dd5566;
  text-shadow: none;
  border: none; }

.reveal .roll span:after {
  color: #fff;
  background: #6a1520; }

/*********************************************
 * IMAGES
 *********************************************/
.reveal section img {
  margin: 15px 0px;
  background: rgba(255, 255, 255, 0.12);
  border: 4px solid #eee;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.15); }

.reveal section img.plain {
  border: 0;
  background: none;
  box-shadow: none; }

.reveal a img {
  -webkit-transition: all .15s linear;
  -moz-transition: all .15s linear;
  transition: all .15s linear; }

.reveal a:hover img {
  background: rgba(255, 255, 255, 0.2);
  border-color: #a23;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.55); }

/*********************************************
 * NAVIGATION CONTROLS
 *********************************************/
.reveal .controls {
  color: #a23; }

/*********************************************
 * PROGRESS BAR
 *********************************************/
.reveal .progress {
  background: rgba(0, 0, 0, 0.2);
  color: #a23; }

.reveal .progress span {
  -webkit-transition: width 800ms cubic-bezier(0.26, 0.86, 0.44, 0.985);
  -moz-transition: width 800ms cubic-bezier(0.26, 0.86, 0.44, 0.985);
  transition: width 800ms cubic-bezier(0.26, 0.86, 0.44, 0.985); }

/*********************************************
 * PRINT BACKGROUND
 *********************************************/
@media print {
  .backgrounds {
    background-color: #222; } }

.reveal p {
  font-weight: 300;
  text-shadow: 1px 1px #222; }

.reveal h1,
.reveal h2,
.reveal h3,
.reveal h4,
.reveal h5,
.reveal h6 {
  font-weight: 700; }

.reveal p code {
  background-color: #23241f;
  display: inline-block;
  border-radius: 7px; }

.reveal small code {
  vertical-align: baseline; }
  
/************************************************
 Added by Jacky Baltes
 ************************************************/
.jb-slide {
  text-align: center;
}

.jb-center {
  text-align:center;
}

.jb-very-small {
  display: inline-block;
  font-size: 0.5em;
  line-height: 1.0em;
  vertical-align: top; }
  
.jb-footer-right {
  position: absolute;
  bottom: 0px;
  right: 0px;
  width: auto;
  height: 1cm;
  max-height: 1cm;
}

.jb-footer-right-img {
  border: none;
  background: none;
  box-shadow: none;
  width: auto;
  height: 1.25cm;
}

.jb-footer-left {
  position: absolute;
  bottom: 0px;
  left: 0px;
  width: auto;
  height: 1cm;
  max-height: 1cm;
}

.jb-footer-left-img {
  border: none;
  background: none;
  box-shadow: none;
  width: auto;
  height: 1.25cm;
}
"""

with cd(ROOT_DIR):
    with open("reveal.js/css/theme/ntnuerc.css","w") as f:
        f.write(ntnuRevealTheme)

from IPython.core import magic_arguments
from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class
from IPython.core.display import HTML, Image, Pretty, Javascript, display
from IPython.utils.capture import capture_output

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

from jinja2 import Template

#import weasyprint as wp
import io
import base64

from docutils import core, io

import zipfile
import os

# Based on reveal.js 3.7.0
REVEAL_PRESENTATION_TEMPLATE = """
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

REVEAL_SLIDE_TEMPLATE = """
<section id="{{id}}">

{{slideHTML}}

<aside class="notes">
{{slideNote}}
</aside>

{{slideChildren}}

</section>
"""

from urllib import request
#from google.colab import files
import pathlib
import youtube_dl

from .jbdata import JBImage
from .jbdata import JBVideo

robbi = JBImage( name='robbi', width=162, height=138, url="https://i.postimg.cc/K81kVbvQ/ntnuerc-logo-1.png", localFile= ROOT_DIR / "reveal.js" / "assets" / "images" / "robbi.png" )
logo = JBImage( name = 'logo', width=0, height=0, url='https://i.postimg.cc/4xvjvdmq/ntnu-ee-logo.png', localFile=ROOT_DIR / "reveal.js" / "assets" / "images" / "logo.png" )

RenpyInitTemplate = """
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

RenpyScriptTemplate = """
# Slide {{id}}
label {{label}}:
    scene bg {{id}} with {{transition}}
{{renpy}}
    jump {{right}}
"""

RenpyTransition = "fade"
RenpyInitLabel = ".init"

from .jbslide import JBSlide

import pathlib

THEME="ntnuerc"
RevealSlideFooter = """
<footer>
<div class="jb-footer-left">
    <img class="jb-footer-left-img plain" src="{{ logo.url }}" alt="{{logo.name}}" />
</div>
<div class="jb-footer-right">
    <img class="jb-footer-right-img plain" src="{{ robbi.url }}" alt="{{robbi.name}}" />
</div>
</footer>
"""

import re
import pathlib

def makeRevealThemeLocal( revealTheme ):
    """removes .reveal, .reveal .slides, and .reveal .slides section from theme css"""
    themePath = pathlib.Path( str(ROOT_DIR) +  '/reveal.js' +  '/css/theme/' + THEME + '.css' )
    with open( themePath ) as f:
        css = f.read()
    for x,r in [ ( "\.reveal \.slides section ", ".jb-render " ), 
                ("\.reveal \.slides ", ".jb-render " ), 
                ("\.reveal ", ".jb-render " ), 
                ("section", ".jb-render ") ]:
        css = re.sub(x, r, css)
    return css

codeCellCSS = """
.jb-input-code {
    color: #101010;
    width: 90%;
    display: inline-block;
}

.jb-stdout {
    color: #101010;
    background: #e0e0e0;
    width: 90%;
    display: inline-block;
}
"""

from .jbdocument import JBDocument

localTheme = makeRevealThemeLocal( "/theme/" + THEME ) + codeCellCSS 
#print("local css", localTheme)

@magics_class
class JackyMagics(Magics):
    def __init__(self, shell, doc ):
        super(JackyMagics, self).__init__(shell)
        self.doc = doc
      
    def instTemplate( self, text, vars ):
        return JBDocument.sInstTemplate( text, { **self.shell.user_ns, **vars } )
      
    def html_parts(self, input_string, source_path=None, destination_path=None,
               input_encoding='unicode', doctitle=True,
               initial_header_level=1):
        """
    Given an input string, returns a dictionary of HTML document parts.

    Dictionary keys are the names of parts, and values are Unicode strings;
    encoding is up to the client.

    Parameters:

    - `input_string`: A multi-line text string; required.
    - `source_path`: Path to the source file or object.  Optional, but useful
      for diagnostic output (system messages).
    - `destination_path`: Path to the file or object which will receive the
      output; optional.  Used for determining relative paths (stylesheets,
      source links, etc.).
    - `input_encoding`: The encoding of `input_string`.  If it is an encoded
      8-bit string, provide the correct encoding.  If it is a Unicode string,
      use "unicode", the default.
    - `doctitle`: Disable the promotion of a lone top-level section title to
      document title (and subsequent section title to document subtitle
      promotion); enabled by default.
    - `initial_header_level`: The initial level for header elements (e.g. 1
      for "<h1>").
        """
        overrides = {'input_encoding': input_encoding,
                     'doctitle_xform': doctitle,
                     'initial_header_level': initial_header_level}
        parts = core.publish_parts(
            source=input_string, source_path=source_path,
            destination_path=destination_path,
            writer_name='html', settings_overrides=overrides)
        return parts

      
    def html_body(self, input_string, source_path=None, destination_path=None,
              input_encoding='unicode', output_encoding='unicode',
              doctitle=True, initial_header_level=1):
        """
    Given an input string, returns an HTML fragment as a string.

    The return value is the contents of the <body> element.

    Parameters (see `html_parts()` for the remainder):

    - `output_encoding`: The desired encoding of the output.  If a Unicode
      string is desired, use the default value of "unicode" .
        """
        parts = self.html_parts(
            input_string=input_string, source_path=source_path,
            destination_path=destination_path,
            input_encoding=input_encoding, doctitle=doctitle,
            initial_header_level=initial_header_level)
        fragment = parts['html_body']
        if output_encoding != 'unicode':
            fragment = fragment.encode(output_encoding)
        return fragment

    def embedCellHTML( self, html, line, cls, css ):
        it = "" 
        
        if css:
            it = it + "<style>\n" + css + "\n" + "</style>" + "\n"
        
        it = it + '<div class="{cls} jb-render">\n'.format(cls=cls)

        if line:
            #print("Adding style", line)
            it = it + "<div {0}>\n".format(line)
        #it = it + "<div class=\"reveal\">"
        #it = it + "    <div class=\"slides\">"
        #it = it + "        <section>"
        
        it = it + html + "\n"

        #it = it + "        </section>"
        #it = it + "    </div>"
        #it = it + "</div>"
        
        it = it + '</div>\n'
        #it = it + """
        #          <script src="reveal.js/js/reveal.js"></script>
		    #          <script>
			  #             Reveal.initialize();
		    #          </script>
        #"""
        if line:
            it = it + "</div>\n"
        #print(self.shell.user_ns['test'])
        #print(s
        return it
      
    def createHTMLRepr( self, output ):
        rh = getattr( output, "_repr_html_", None )
        if ( callable( rh ) ):
            html = output._repr_html_()
            if ( html is not None ):
                return html
            else:
                rp = getattr( output, "_repr_png_", None )
                if ( callable(rp) ):
                    png = output._repr_png_()
              
                    if ( png is not None ):
                        enc = base64.b64encode(png).decode('utf-8')
                        
                        return '<img src="data:image/png;base64,{0}"></img>'.format(enc)
        return None
      
    @cell_magic
    def html_templ(self, line, cell ):
        it = ""
        if line:
            it = it + "<div {0}>\n".format(line)
        it = it + cell + "\n"
        if line:
            it = it + "</div>\n"
        #print(self.shell.user_ns['test'])
        #print(s)
        display(HTML( self.instTemplate(it, {}) ) )
    
    @cell_magic
    def reveal_html(self, line, cell ):      
        it = self.embedCellHTML( cell, line, 'jb-output', localTheme )
        display( HTML( self.instTemplate(it, { } ) ) )

    @cell_magic
    def reveal_rst(self, line, cell ):      
        
        md = self.html_body( input_string = cell )

        it = self.embedCellHTML( md, line, 'jb-output', localTheme )
        
        display( HTML( self.instTemplate(it, {} ) ) )

    @cell_magic
    def css( self, line, cell ):
        s = ""
        s = s + "<style>" + "\n"
        s = s + self.instTemplate(cell, {} )
        s = s + "</style>" + "\n"
        display( HTML(s) )
        
        
    @magic_arguments.magic_arguments()
    @magic_arguments.argument('--no-stderr', action="store_true",
        help="""Don't capture stderr."""
    )
    @magic_arguments.argument('--no-stdout', action="store_true",
        help="""Don't capture stdout."""
    )
    @magic_arguments.argument('--no-display', action="store_true",
        help="""Don't capture IPython's rich display."""
    )
    @magic_arguments.argument('--echo', action="store_true",
        help="""Prepend cell content."""
    )
    @magic_arguments.argument('--parent', type=str, default='', 
        help="""Select parent slide. Slide will be appended to list of children of this slide"""
    )
    @magic_arguments.argument('--id', type=str, default='', 
        help="""Select slide id"""
    )
    @magic_arguments.argument('--footer', type=str, default='', nargs=1, 
        help="""Define the slide footer"""
    )
    @magic_arguments.argument('--header', type=str, default='', nargs=1, 
        help="""Define the slide header"""
    )
    @magic_arguments.argument('--background', type=str, default='', nargs=1, 
        help="""Define the slide background"""
    )
    @magic_arguments.argument('--output', type=str, default='output', nargs=1,
        help="""A variable that will be pushed into the user namespace with the 
        utils.io.CapturedIO object.
        """
    )
    @magic_arguments.argument('--style', type=str, default='',
        help="""
        HTML inline style to be applied to the cell.
        """
    )
    
    @cell_magic
    def slide( self, line, cell):
        args = magic_arguments.parse_argstring(self.slide, line)
        out = not args.no_stdout
        err = not args.no_stderr
        disp = not args.no_display
        
        #print('args', args )

        if ( args.style ):
            if args.style[0] == '"' or args.style[0] == "'":
                args.style = args.style[1:]
            if args.style[-1] == '"' or args.style[-1] == "'":
                args.style = args.style[0:-1]
            
            mystyle = 'style="{s}"'.format(s=args.style)
        else:
            mystyle = ""
            
        #print("MYSTYLE", mystyle)
            
        s = self.instTemplate( cell, {} )
        with capture_output(out, err, disp) as io:
            self.shell.run_cell(s)
        
        html = '<div class="{cls}" id="{id}">\n'.format(cls="jb-slide", id=args.id)
        
        #print(args.echo)
        if ( args.echo ):
            html = html + '<div class="jb-input jb-render jb-code" style="text-align:center">' + '\n'
            html = html + self.embedCellHTML( highlight( cell, PythonLexer(), HtmlFormatter( cssstyles="color:#101010;display=inline-block;", noclasses=True ) ), mystyle, 'jb-input-code', localTheme ) + '\n'
            html = html + "</div>" + "\n"
        #print("html", html)

        if ( out ):
            if io.stdout != "":
                #print("Adding output", io.stdout)
                h = '<div class="jb-output jb-render code" style="text-align:center">' + '\n'
                h = h  + '<div class="jb-stdout code" style="display:inline-block; width:90%">' + '\n'
                h = h + '<pre {s}>\n'.format(s = mystyle)
                h = h + io.stdout
                h = h + '</pre>\n'
                h = h + '</div>\n'           
                h = h + '</div>\n'
                html = html + self.embedCellHTML( h, mystyle, 'jb-print', '' )
                
        for o in io.outputs:
            #print('Output', o)
            h = self.createHTMLRepr( o )
            #print('SLIDE: h', h)
            if ( h is not None ):
                html = html + "\n" + self.embedCellHTML( h, mystyle, 'jb-output-code', '' ) + "\n"
        
        html = html + "\n" + "</div>"

        #html = re.sub("<style>.*", "", html, flags=re.MULTILINE )
        #htmlNoStyle=html
        #if ( html.find("<style>") >= 0 ) and  ( html.find("</style>") >= 0 ):
        #    htmlNoStyle = html[:html.find("<style>")] + html[html.find("</style>") + len("</style>"):]
        #print('*** HTML ***', html)
        
        if args.output:
            self.shell.user_ns[args.output] = html

        slide = self.doc.addSlide( args.id, html, args.background, args.header, args.footer )
        
        #print(t)
        display( HTML( '<style>\n' + localTheme + '\n' + '</style>' + '\n' + slide.html ) )
        #display( Image(slide.image ) )
        
        
    @magic_arguments.magic_arguments()
    @magic_arguments.argument('--id', type=str, default='', 
        help="Select slide id. Use current slide if unspecified."
    )
    @magic_arguments.argument('--label', type=str, default='', 
        help="Select start label for renpy script of this slide"
    )
    
    @cell_magic
    def renpy( self, line, cell):
        args = magic_arguments.parse_argstring(self.renpy, line)
        RENPY_INDENT = 4
        it = ""
        if args.label:
            it = it + "\n" + "label" + " " + args.label + ":"
            indent = 2 * RENPY_INDENT
        else:
            indent = RENPY_INDENT
        cellText = "\n".join( [ " " * indent + c if (len(c) > 0 ) else "\n" for c in cell.splitlines() ] )
        it = it + cellText + "\n"
        
        #print(self.shell.user_ns['test'])
        #print(s)
        rp = self.instTemplate( it, {} )
        display( Pretty( rp ) )
        cs = doc.getCurrentSlide()
        if ( cs ):
            #print("*** Adding renpy to slide ", cs.id )
            #print(rp)
            
            cs.addRenpy( rp )
    
def load_ipython_extension(ipython):
    """
    Any module file that define a function named `load_ipython_extension`
    can be loaded via `%load_ext module.path` or be configured to be
    autoloaded by IPython at startup time.
    """
    # This class must then be registered with a manually created instance,
    # since its constructor has different arguments from the default:
    
    ratio = 1.0
    PAGE_SIZE=( int( 1280 * ratio ), int( 720 * ratio ) )

    cssStr = """
        @page {{
            size: {width}px {height}px;
            margin: 0px;
        }}""".format( width=PAGE_SIZE[0], height=PAGE_SIZE[1] )

    footer = RevealSlideFooter
    doc = JBDocument( title, cssStr + "\n" + localTheme, footer = footer )
    magics = JackyMagics( ipython, doc )
    doc.user_ns = magics.shell.user_ns
    ipython.register_magics(magics)
    return doc

doc = load_ipython_extension( get_ipython() )

email="jacky.baltes@ntnu.edu.tw"
author = """
<p>
      Jacky Baltes<br>
      National Taiwan Normal University<br>
      Taipei, Taiwan<br>
      <a href="mailto:{{email}}">{{email}}</a><br>
      {{today}}
</p>
"""

"""%%slide --id=first
%%reveal_html

<h1> {{title}}</h1>

   <div class="author" style="text-align:center;">
    {{author}}
   </div>
"""

vid1 = JBVideo( 'video1', 0, 0, url='https://youtu.be/OVcwcvwzRPs?t=28', localFile= ROOT_DIR / "reveal.js" / "assets" / "videos" / "video1" )

