from urllib import request
import pathlib
import base64
import youtube_dl
import uuid

cfg = {}

class JBData:
    """
    Class that encapsulates an image and its various representations.
    """

    JBDATA, JBIMAGE_PNG, JBIMAGE_SVG, JBIMAGE_JPG, JBVIDEO = 0, 10, 11, 12, 30

    @staticmethod
    def sReadDataFromURL(url):
        data = request.urlopen(url).read()
        return data

    @staticmethod
    def sReadData( fname ):
        #print('JBData.sReadData', 'Reading file', fname)
        with open( fname, "rb") as f:
            data = f.read()
        return data

    @staticmethod
    def sWriteData(fname, data):
        with open(fname, "wb") as f:
            f.write(data)

    def getDefaultFileName(self):
        p = cfg['ROOT_DIR'] / 'reveal.js' / 'assets' / "{name}.{suffix}".format(name=self.name, suffix=self.suffix)
        return str(  p.expanduser().resolve() )

    def __init__(self, name, url=None, data=None, localFile=None, atype = JBDATA, suffix="dat"):
        self.url = url
        self.name = name
        self.suffix = suffix
        self.data = None
        self.ids = []
        self.type = atype

        if data:
            if not localFile:
                localFile = self.getDefaultFileName()
            with open(localFile, "wb") as f:
                f.write(data)
                self.localFile = localFile
        elif url:
            if not localFile:
                localFile = self.getDefaultFileName()
            self.data = self.readDataFromURL(url, localFile)
            if (self.data):
                JBData.sWriteData(localFile, self.data)
            self.localFile = localFile
        elif localFile:
            data = JBData.sReadData( str(localFile) + "." + suffix)
            print('localFile', str(localFile) + "." + suffix)
            self.localFile = localFile
        else:
            uploaded = files.upload()
            for fn in uploaded.keys():
                print('User uploaded file "{name}" with length {length} bytes'.format(
                    name=fn, length=len(uploaded[fn])))
                self.localFile = fn
        self.clearCache()

    def readDataFromURL(self, url, tmpFile):
        # print('JBData.readDataFromURL', url )
        return JBData.sReadDataFromURL(url)

    def writeData(self, rdir):
        if (self.localFile):
            fname = self.localFile
        else:
            fname = self.getDefaultFileName()
        if (not self.data):
            self.data = JBData.sReadData(fname)
        ret = JBData.sWriteData(pathlib.Path(rdir).joinpath(fname), self.data)
        self.clearCache()
        return ret

    def readData( self ):
        if ( self.localFile ):
            fname = self.localFile
            self.data = sReadData( fname )
            
    @staticmethod
    def getBase64Data(fname):
        data = JBData.sReadData(fname)
        enc = base64.b64encode(data).decode('utf-8')
        return enc

    def clearCache(self):
        if (self.data) and (len(self.data) > 1024 * 1024):
            self.data = None

    @staticmethod
    def sCreateStyleString(typ, st):
        if st:
            s = typ + '="{}"'.format(st)
        else:
            s = ""
        return s

    def createStyleString( self, typ, st ):
        return JBData.sCreateStyleString( typ, st )

    def __repr_html__(self, cls=None, style = None):
        id = self.generateId()
        if id not in self.ids:
            self.ids.append( id )
        s = self.createStyleString( "class", cls ) + " " + self.createStyleString( "style", style )
        return '<a id="{0}" {2} href="{1}"></a>'.format(self.name, self.url, s )

    def __call__(self, cls=None, style = None ):
        return self.__repr_html__(cls, style)

    @staticmethod
    def sGenerateId():
        return "id-" + str( uuid.uuid4() )

    def generateId( self ):
        return JBData.sGenerateId()

class JBImage(JBData): 
    def __init__(self, name, width, height, url=None, data=None, localFile=None, suffix=None):
        if ( not suffix ):
            if ( localFile ):
                if str(localFile)[-4:] == ".png":
                    suffix = "png"
                elif str(localFile)[-4:] == ".svg":
                    suffix = "svg"
                elif str(localFile)[-4:] == ".jpg":
                    suffix = "jpg"
                elif str(localFile)[-5:] == ".jpeg":
                    suffix = "jpeg"
                
        if ( localFile and str(localFile)[-len(suffix) + 1:] == "." + suffix ):
            localFile = str(localFile)[0:-len(suffix) + 1]
        if suffix == 'png':
            atype = JBData.JBIMAGE_PNG
        elif suffix == "svg":
            atype = JBData.JBIMAGE_SVG
        elif suffix == "jpg" or suffix == "jpeg":
            atype = JBData.JBIMAGE_JPG
        else:
            print('name', name, 'localFile', localFile, 'suffix', suffix)
            raise Exception("Unknown JBImage data type: " + suffix )
        super(JBImage, self).__init__(name, url, data, localFile, atype=atype, suffix=suffix)
        self.width = width
        self.height = height

    def __repr_html_file__(self, cls = None, style=None):
        id = self.generateId()
        w = self.createWidthString()
        h = self.createHeightString()
        if id not in self.ids:
            self.ids.append( id )
        cs = self.createStyleString( "class", cls ) + " " + self.createStyleString( "style", style )
        rpath = str( pathlib.Path(self.localFile).relative_to(cfg['REVEAL_DIR'] ) )
        return '<span id="{id}" {style}><img id="img-{id}" {width} {height} src="http://localhost:{port}/{src}"/></span>\n'.format( id=id, width=w, height=h, style=cs, port=cfg['HTTP_PORT'], src=rpath + "." + self.suffix )

    def __repr_html_url__(self, cls=None, style=None):
        id = self.generateId()
        w = self.createWidthString()
        h = self.createHeightString()
        if id not in self.ids:
            self.ids.append( id )
        cs = self.createStyleString( "class", cls ) + " " + self.createStyleString( "style", style )
        return '<span id="{id}" {style}><img id="img-{id}" {width} {height} src="{url}"/></span>\n'.format(id=id, width=w, height=h, url=self.url, style=cs )        

    def __repr_html_base64__(self, cls=None, style=None):
        id = self.generateId()
        w = self.createWidthString()
        h = self.createHeightString()
        if id not in self.ids:
            self.ids.append( id )
        cs = self.createStyleString( "class", cls ) + " " + self.createStyleString( "style", style )
        return '<span id="{id}" {style}><img id="img-{id}" {width} {height} src="data:image/png;base64,{src}"/></span>\n'.format(id=id, width=w, height=h, style=cs, src=JBData.getBase64Data( str(self.localFile) + "." + self.suffix ) )

    def __repr_html_svg__(self, cls=None, style=None):
        id = self.generateId()
        w = self.createWidthString()
        h = self.createHeightString()
        if id not in self.ids:
            self.ids.append( id )
        cs = self.createStyleString( "class", cls ) + " " + self.createStyleString( "style", style )
        data = JBData.sReadData( str(self.localFile) + "." + self.suffix ).decode('utf-8')
        return '<span id="{id}" {style}>{data}</span>\n'.format(id=id, width=w, height=h, style=cs, data=data )

    def getDefaultFileName(self):
        p = cfg['REVEAL_IMAGES_DIR'] /  "{name}.{suffix}".format(name=self.name, suffix=self.suffix)
        return str(  p.expanduser().resolve() )

    @staticmethod
    def sCreateWidthString( width ):
        if width > 0:
            w = "width={0}".format(width)
        else:
            w = ""
        return w

    def createWidthString( self ):
        return JBImage.sCreateWidthString( self. width )        

    @staticmethod
    def sCreateHeightString( height ):
        if height > 0:
            h = "height={0}".format(height)
        else:
            h = ""
        return h
    
    def createHeightString( self ):
        return JBImage.sCreateHeightString( self.height )

    def __repr_html__(self, cls = None, style=None):
        s = ""
        if ( self.type == JBData.JBIMAGE_SVG ):
            s = self.__repr_html_svg__( cls, style )
        elif ( ( cfg['HTTPD'] ) and ( cfg['HTTP_PORT'] >= 0 ) and self.localFile ):
            s = self.__repr_html_file__( cls, style )
        elif  ( ( cfg['HTTP_PORT'] >= 0 ) and self.localFile ):
            s = self.__repr_html_base64__( cls, style )
        elif self.url:
            s = self.__repr_html_url__( cls, style )
        return s

class JBVideo(JBData):
    def __init__(self, name, width, height, url=None, data=None, localFile=None, suffix="webm"):
        super(JBVideo, self).__init__(name, url, data, localFile, atype=JBData.JBVIDEO, suffix=suffix)
        self.width = width
        self.height = height

    def __repr_html_file__(self, style=""):
        return """<video controls>
                    <source src="{src}" style="{style}">'
                    </video>
                 """.format(src=self.localFile, port=cfg['HTTP_PORT'], name=self.name, style=style)

    def readDataFromURL( self, url, localFile ):
        print('Reading video from', url)
        ydl_opts = {'outtmpl': localFile }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        self.localFile = localFile

    def getDefaultFileName(self):
        p = cfg['REVEAL_VIDEOS_DIR'] /  "{name}.{suffix}".format(name=self.name, suffix=self.suffix)
        return str(  p.expanduser().resolve() )

    def __repr_html__(self, cls = None, style=None):
        id = self.generateId()
        w = self.createWidthString()
        h = self.createHeightString()
        if id not in self.ids:
            self.ids.append( id )
        cs = self.createStyleString( "class", cls ) + " " + self.createStyleString( "style", style )
        return '''<span id="{id}" {style}>
            <iframe id="vid-{id}" {width} {height} src="{src}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </span>\n'''.format(id=id, width=w, height=h, src=self.url, style=cs )

    def __repr_html_localhost_(self, cls = None, style=None):
        id = self.generateId()
        w = self.createWidthString()
        h = self.createHeightString()
        if id not in self.ids:
            self.ids.append( id )
        cs = self.createStyleString( "class", cls ) + " " + self.createStyleString( "style", style )
        return '''<span id="{id}" {style}>
           <video id="vid-{id}" controls>
           <source src="{src}"/>
           </span>\n'''.format(id=id, width=w, height=h, src=self.url, style=cs )

    def createHeightString( self ):
        return JBImage.sCreateHeightString( self.height )
    
    def createWidthString( self ):
        return JBImage.sCreateWidthString( self.width )


def createEnvironment( mycfg ):
    global cfg
    cfg = mycfg
    return cfg
