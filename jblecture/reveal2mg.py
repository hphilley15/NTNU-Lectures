"""
A module that converts a reveal slideshow to a monogatari visual novel.
"""
import bs4
from bs4 import BeautifulSoup
import sys
import re

slideNum = 0

class Slide:
    def __init__(self, id = "", html = "", dialog = "" ):
        global slideNum
        slideNum = slideNum + 1
        if id == "":
            id = "slide_{0:5d}".format(slideNum)
        self.id = id
        self.html = html
        self.dialog = dialog
        self.children = []

    def addChild( self, sl ):
        self.children.append( sl )

class MGDocParser():
    def __init__(self):
        self.slides = []
        self.soup = None
        self.root = None

    def parseFile0( self, root, soup ):
        for c in soup.find_all("section"):
            #print('Found slide', c['id'] )
            slide = c.find( "div", class_ = "jb-slide")
            if ( slide ):
                html = slide
                d = c.find( "aside", class_ = "notes" )
                if ( d ):
                    dialog = self.parseRenpy( d.get_text() )
                else:
                    dialog = ""
                root.addChild( self.parseFile0( Slide( c['id'], html, dialog ), slide ) )
        return root

    def parseFile( self, fname ):
        with open( fname, "r") as f:
            self.soup = BeautifulSoup( f )
            slides = self.soup.find( "div", class_ = 'slides' )
            self.root = self.parseFile0( Slide("ROOT", "", "" ), slides )

    def printTree( self, node = None, level = 0 ):
        if not node:
            node = self.root
        #print("type", type(node))
        print("   " * level, node.id )
        #print("   " * level, node.html )
        print("   " * level, node.dialog )
        for c in node.children:
            self.printTree( c, level + 1 )

    def parseRenpy(self, dialog ):
        out = ""
        for d in dialog.splitlines():
            d.replace('"', '').lstrip().rstrip()
            print(d)
            line = ""
            if d:
                line = line + '"'
                line = line + d
                line = line + '"'
                line = line + ','
            if ( line ):
                out = out + line + '\n'
        return [ f for f in filter(lambda x: not re.match(r'^\s*$', x), out.splitlines() ) ]

def main( args = None ):
    if args is None:
        args = sys.argv[1:]
    parser = MGDocParser()
    parser.parseFile( args[0] )
    parser.printTree( )

if __name__ == "__main__":
    main( [ "C:/Users/negri/Desktop/reveal.js/index.html" ] )