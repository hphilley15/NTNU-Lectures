class JBData:
    """
    Class that encapsulates an image and its various representations.
    """

    @staticmethod
    def sReadDataFromURL(url):
        data = request.urlopen(url).read()
        return data

    @staticmethod
    def sReadData(name):
        with open(name, "rb") as f:
            data = f.read()
        return data

    @staticmethod
    def sWriteData(fname, data):
        with open(fname, "wb") as f:
            f.write(data)

    def getDefaultFileName(self):
        return DATA_DIR + "/{name}{ext}".format(name=name, ext=self.ext)

    def __init__(self, name, url=None, data=None, localFile=None, ext=".dat"):
        self.url = url
        self.name = name
        self.ext = ext
        self.data = None
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
            self.localFile, self.ext = pathlib.Path(localFile)
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

    @staticmethod
    def getBase64Data(fname):
        data = JBData.sReadData(fname)
        enc = base64.b64encode(data).decode('utf-8')
        return enc

    def clearCache(self):
        if (self.data) and (len(self.data) > 1024 * 1024):
            self.data = None


class JBImage(JBData):
    def __init__(self, name, width, height, url=None, data=None, localFile=None):
        super(JBImage, self).__init__(name, url, data, localFile, ext=".png")
        self.width = width
        self.height = height

    def __repr_html_file__(self, style=""):
        return '<img src="http://localhost:{port}/{src}{ext}" style="{style}" alt="{name}"/>'.format(src=self.localFile,
                                                                                                     ext=self.ext,
                                                                                                     port=HTTP_PORT,
                                                                                                     name=self.name,
                                                                                                     style=style)

    def __repr_html_url__(self, style=""):
        return '<img src="{src}" style="{style}" alt="{name}"/>'.format(src=self.url, name=self.name, style=style)

    def __repr_html_b64__(self, style=""):
        return '<img src="data:image/png;base64,{src}" style="{style}" alt="{name}"/>'.format(
            src=JBData.getBase64Data(self.localFile), name=self.name, style=style)

    def getDefaultFileName(self):
        return IMAGES_DIR + "/{name}{ext}".format(name=name, ext=self.ext)


class JBVideo(JBData):
    def __init__(self, name, width, height, url=None, data=None, localFile=None):
        super(JBVideo, self).__init__(name, url, data, localFile, ext=".mp4")
        self.width = width
        self.height = height

    def __repr_html_localhost__(self, style=""):
        return """<video controls>
                    <source src="http://localhost:{port}/{src}{ext}" style="{style}">'
                    </video>
                 """.format(src=self.localFile, ext=self.ext, port=HTTP_PORT, name=self.name, style=style)

    def __repr_html_file__(self, style=""):
        return """<video controls>
                    <source src="{src}{ext}" style="{style}">'
                    </video>
                 """.format(src=self.localFile, ext=self.ext, port=HTTP_PORT, name=self.name, style=style)

    def readDataFromURL(self, url, localFile=None):
        print('Reading video from', url)
        ydl_opts = {'outtmpl': str(localFile)}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def getDefaultFileName(self):
        return VIDEOS_DIR + "/{name}{ext}".format(name=name, ext=self.ext)
