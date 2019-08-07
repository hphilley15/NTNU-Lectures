import weasyprint as wp
from jinja2 import Template
import re
import pathlib

from ..jbslide import JBSlide

class JBDocument:
    def __init__(self, background = '', footer = '', header = '' ):
        self.slides = []
        self.renpy = []
      
        self.current = ''
        self.parent = ''
        
        self.slideCount = 1
        self.slideFragmentCount = 1
        
        self.user_ns = {}
        
        # self.setTheme( theme )
        # self.setFooter( footer )
        # self.setHeader( header )
        # self.setBackground( background )

    # def setFooter(self, footer ):
    #     self.footer = footer

    # def setHeader(self, header):
    #     self.header = header

    # def setBackground( self, bg ):
    #     self.background = bg

    def createLocalTheme( self ):
        return self.makeRevealThemeLocal( self.theme )
            
    def makeRevealThemeLocal(self, revealTheme):
        """removes .reveal, .reveal .slides, and .reveal .slides section from theme css"""
        tname = cfg['REVEAL_THEME'] + '.css' 
        themePath = pathlib.Path( cfg['ROOT_DIR'] / 'reveal.js' / 'css' / 'theme' / tname ).resolve()
        with themePath.open() as f:
            css = f.read()
        for x, r in [("\.reveal \.slides section ", ".jb-render "),
                     ("\.reveal \.slides ", ".jb-render "),
                     ("\.reveal ", ".jb-render "),
                     ("section", ".jb-render ")]:
            css = re.sub(x, r, css)
        return css

    @staticmethod
    def sInstTemplate( text, vars ):
        prev = ""
        current = text
        while( prev != current ):
            t = Template( current )
            prev = current
            current = t.render( vars )
        return current 
      
    def instTemplate( self, text, vars ):
        d = { **self.user_ns, **vars }
        d['cfg'] = cfg
        return JBDocument.sInstTemplate( text, d )
        
    def findSlideIndex( self, id ):
        #print('Looking for', id)
        try:
            ind = next(i for i,v in enumerate( self.slides ) if v.id == id )
        except StopIteration:
            ind = -1
        #print('returning', ind )
        return ind

    def addSlide( self, id, slideHTML, background = '', header = '', footer = ''):
        #html = wp.HTML( string = slideHTML )
        #doc = html.render( stylesheets = [ self.cssSlides ] )
        #png, width, height = doc.write_png( target=None )
        
        if ( not background ):
            background = self.instTemplate( self.background, {} )
        
        if ( not header ):
            header = self.instTemplate( self.header, {} ) 
            
        if ( not footer ):
            footer = self.instTemplate( self.footer, {} )
            
        self.slideCount = self.slideCount + 1
        self.slideFragmentCount = 1
        
        if ( id == "" ):
            id = "slide_{0:05d}_frag_{1:05d}".format( self.slideCount, self.slideFragmentCount )
        
        if ( id[0] == '"' ) or ( id[0] == "'" ):
            id = id[1:]
        if ( id[-1] == '"' ) or ( id[-1] == "'" ):
            id = id[:-1]
            
        oind = self.findSlideIndex( id )
        if (  oind >= 0 ) and ( oind < len(self.slides) ):
            del self.slides[oind]
        
        #print("footer", footer )
        sl = JBSlide( id, header + '\n' + background + '\n' + slideHTML + '\n' + footer, renpy = '', left='', right='', up='', down='' )
        
        if ( self.current != '' ):
            leftS = self.slides[ self.findSlideIndex( self.current ) ]
            leftS.right = sl.id
            sl.left = self.current
        
        self.current = id
        self.slides.append( sl )
        return sl
        
    def getCurrentSlide( self ):
        slide = None
        idx = self.findSlideIndex( self.current )
        if ( idx >= 0 ) and ( idx < len( self.slides ) ):
            slide = self.slides[idx]
        return slide
        
    def numberOfSlides( self ):
        return ( len( self.slides ) )
    
    def createSlides( self, start ):
        s = self.slides[ self.findSlideIndex( start ) ]
        slides = s.__repr_reveal_html__()
        
        while( s.right != '' ):
            s = self.slides[ self.findSlideIndex( s.right ) ]
            slides = slides + s.__repr_reveal_html__()
        return slides
      
    def createRevealSlideShow(self, startId = None ):
        if ( not startId ):
            startId = self.slides[0].id
        slides = self.createSlides( startId )
        presentation = self.instTemplate( cfg['REVEAL_PRESENTATION_TEMPLATE'], { 'title': cfg['TITLE'], 'slides': slides } )
        return presentation
    
    def createRevealDownload( self, dir, fname = 'index.html' ):
        html = self.createRevealSlideShow()
        with open( pathlib.Path( dir ).joinpath( fname ), "w" ) as f:
            f.write( html )
    
    def createSlideImages(self, rdir ):
        for s in self.slides:
            img = s.createJBImage( self.cssSlides )
            img.writeData( rdir )
    
    def createBackgroundsFile( self, rdir ):
        with open( pathlib.Path( rdir ).joinpath( "backgrounds.rpy" ), "w" ) as f:
            for s in self.slides:
                fname = s.getImageFileName()
                p = pathlib.Path( fname )
                rp = pathlib.Path(* p.parts[1:])
                f.write( f'image bg {s.id} = "{ str(rp) }"\n' )

    def createScriptFiles( self, rdir, startId = None ):
        if ( not startId ):
            startId = self.slides[0].id
        
        rpyScript = self.instTemplate( cfg['RenpyInitTemplate'], { 'title': cfg['TITLE'], 'startId': startId } )
        sp = pathlib.Path( rdir ) / "start.rpy"
        with sp.open( "w" ) as f:
            f.write( rpyScript )

        currentIdx = self.findSlideIndex( startId )

        while ( currentIdx >= 0 ) and ( currentIdx < len( self.slides) ):
            s = self.slides[ currentIdx ]
            if ( s.renpy ):
                print('Slide', s.id, 'has renpy', s.renpy )
            rpyScript = self.instTemplate( cfg['RenpyScriptTemplate'], { 'label': s.id, 'transition': cfg['RenpyTransition'], 'id': s.id, 'renpy': s.renpy, 'right': s.right } )
            sp = pathlib.Path( rdir ) / f"{s.id}.rpy"
            print("Writing renpy script", str(sp) )
            with sp.open( "w" ) as f:
                f.write( rpyScript )

            currentIdx = self.findSlideIndex( s.right )

    def createRenpySlideShow(self, startId = None ):
        rdir = cfg['RENPY_GAME_DIR']
        self.createSlideImages( rdir )
        self.createBackgroundsFile( rdir )
        self.createScriptFiles( rdir, startId )

cfg = {}

def createEnvironment( mycfg ):
    global cfg
    cfg = mycfg
    return cfg
