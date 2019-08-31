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
        p = cfg['ROOT_DIR'] / 'reveal.js' / 'assets' / "{name}{suffix}".format(name=self.name, suffix=self.suffix)
        return str(  p.expanduser().resolve() )

    def __init__(self, name, url=None, data=None, localFile=None, suffix=".dat"):
        self.url = url
        self.name = name
        self.suffix = suffix
        self.data = None
        self.ids = []

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
            data = JBData.sReadData(localFile)
            print('localFile', localFile)
            self.suffix = pathlib.Path( localFile ).suffix
            self.localFile = pathlib.Path(localFile)
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
    def createStyleString(typ, st):
        if st:
            s = typ + '="{}"'.format(st)
        else:
            s = ""
        return s

    def __repr_html__(self, cls=None, style = None):
        id = generateId()
        if id not in self.ids:
            self.ids.append( id )
        s = createStyleString( "class", cls ) + " " + createStyleString( "style", style )
        return '<a id="{0}" {2} href="{1}"></a>'.format(self.name, self.url, s )

    def __call__(self, cls=None, style = None ):
        return self.__repr_html__(cls, style)

    @staticmethod
    def generateId():
        return "id-" + uuid.uuid4()

class JBImage(JBData): 
    def __init__(self, name, width, height, url=None, data=None, localFile=None):
        super(JBImage, self).__init__(name, url, data, localFile, suffix=".png")
        self.width = width
        self.height = height

    def __repr_html_file__(self, style=""):
        return '<img src="http://localhost:{port}/{src}" style="{style}" alt="{name}"/>'.format(src=self.localFile,
                    port=HTTP_PORT, name=self.name, style=style)

    def __repr_html_url__(self, style=""):
#        return '<img src="{src}" style="{style}" alt="{name}"/>'.format(src=self.url, name=self.name, style=style)

        return '<img src="{src}"'.format(src=self.url )

    def __repr_html_b64__(self, style=""):
        return 'data:image/png;base64,{src}'.format(src=JBData.getBase64Data( self.localFile ) )
#            src=JBData.getBase64Data(self.localFile), name=self.name, style=style)

    def getDefaultFileName(self):
        p = cfg['REVEAL_IMAGES_DIR'] /  "{name}{suffix}".format(name=self.name, suffix=self.suffix)
        return str(  p.expanduser().resolve() )

    @staticmethod
    def createWidthString( width ):
        if self.width > 0:
            w = "width={0}".format(width)
        else:
            w = ""
        return w

    def createWidthString( self ):
        return createWidthString( self. width )        

    @staticmethod
    def createHeightString( height ):
        if self.height > 0:
            h = "width={0}".format(height)
        else:
            h = ""
        return h
    
    def createHeightString( self ):
        return createHeightString( self.height )

    def __repr_html__(self, cls = None, style=None):
        id = generateId()
        w = self.createWidthString()
        h = self.createHeightString()
        if id not in self.ids:
            self.ids.append( id )
        cs = createStyleString( "class", cls ) + " " + createStyleString( "style", style )
        return '<img id="img-{0}" {4} {1} {2} src="{3}"></img>\n'.format(id, w, h, self.url, cs )

class JBVideo(JBData):
    def __init__(self, name, width, height, url=None, data=None, localFile=None):
        super(JBVideo, self).__init__(name, url, data, localFile, suffix=".mp4")
        self.width = width
        self.height = height

    def __repr_html_localhost__(self, style=""):
        return """<video controls>
                    <source src="http://localhost:{port}/{src}" style="{style}">'
                    </video>
                 """.format(src=self.localFile, port=HTTP_PORT, name=self.name, style=style)

    def __repr_html_file__(self, style=""):
        return """<video controls>
                    <source src="{src}" style="{style}">'
                    </video>
                 """.format(src=self.localFile, port=HTTP_PORT, name=self.name, style=style)

    def readDataFromURL(self, url, localFile=None):
        print('Reading video from', url)
        ydl_opts = {'outtmpl': str(localFile)}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def getDefaultFileName(self):
        p = cfg['REVEAL_VIDEOS_DIR'] /  "{name}{suffix}".format(name=self.name, suffix=self.suffix)
        return str(  p.expanduser().resolve() )

def createEnvironment( mycfg ):
    global cfg
    cfg = mycfg
    return cfg
