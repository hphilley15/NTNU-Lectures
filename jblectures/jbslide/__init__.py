class JBSlide:
    def __init__(self, id, html, renpy, left = '', right = '', up = '', down = '', parent = '' ):
        self.id = id
        self.parent = parent
        self.html = html
        
        self.renpy = renpy
      
        self.up = up
        self.left = left
        self.right = right
        self.down = down
        
        self.note = ""

        
    def __repr_reveal_html__( self ):
        reveal = JBDocument.sInstTemplate( REVEAL_SLIDE_TEMPLATE, { 'id': self.id, 'slideHTML': self.html, 'slideNote': self.renpy, 'slideChildren':"" } )
        return reveal
        
    def createJBImage( self, css ):
        html = wp.HTML( string = self.html )
        doc = html.render( stylesheets = [ css ] )
        png, width, height = doc.write_png( target=None )
        img = JBImage( self.id, width, height, data = png, localFile= ROOT_DIR / self.getImageFileName() )
        return img

    def getImageFileName( self ):
        return f"renpy/images/Slides/{self.id}.png"
      
    def addRenpy( self, txt ):
        self.renpy = self.renpy + '\n' + txt
