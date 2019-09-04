var atype = {
    JBDATA : 0,
    JBIMAGE : 1,
    JBVIDEO: 2,    
};

class JBData {
    constructor( name, url=None, data=None, localFile=None, mytype = JBData.atype.JBDATA, suffix=".dat" ) {
        this.mytype = mytype;
        this.name = name;
        this.url = url;
        this.data = data;
        this.localFile = localFile;
        this.suffix = suffix;

        console.log("JBData(" + name + "," + url + "," + localFile + ")" );
    }

    updateAsset( id, mode ) {
        newContent = "";
        if ( mode == "local" ) {
            newContent = "<a id=\"dat-" + id + "\" href=\"file://" + this.localFile + "\">" + this.name + "</a>";
        } else if ( mode == "url" ) {
            newContent = "<a id=\"img-" + id + "\" href=\"" + this.url + "\">" + this.name + "</a>";
        }
        console.log("JBData.updateAsset(" + id + "," + "," + mode + ") =>" + newContent );
        return newContent;
    }    
}

JBData.atype = atype;

class JBImage extends JBData {
    constructor( name, width, height, url=None, data=None, localFile=None ) {
        super( name, url, data, localFile, JBData.atype.JBIMAGE, "png");
        this.width = width;
        this.height = height;
        console.log("JBImage(" + name + "," + url + "," + localFile + ")" );
    }

    updateAsset( id, mode ) {
        var newContent = "";
        if ( mode == "local" ) {
            newContent = "<img id=\"img-" + id + "\" src=\"" + this.localFile + "\"/>";
        } else if ( mode == "url" ) {
            newContent = "<img id=\"img-" + id + "\" src=\"" + this.url + "\"/>";
        }
        console.log("JBImage.updateAsset(" + id + "," + "," + mode + ") =>" + newContent );
        return newContent;
    }    
}

class JBVideo extends JBData {
    constructor( name, width, height, url=None, data=None, localFile=None ) {
        super( name, url, data, localFile, JBData.atype.JBVIDEO, "mp4");
        this.width = width;
        this.height = height;
        console.log("JBVideo(" + name + "," + url + "," + localFile + ")" );
    }

    updateAsset( id, mode ) {
        var newContent = "";
        if ( mode == "local" ) {
            newContent = "<video id=\"vid-" + id + "\" controls> <source src=\"" + this.localFile + "\"/></video>";
        } else if ( mode == "url" ) {
            newContent = "<iframe id=\"vid-" + id + "\" src=\"" + this.url + "\" frameborder=\"0\" allow=\"accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen></iframe>/>";
        }
        console.log("JBVideo.updateAsset(" + id + "," + "," + mode + ") =>" + newContent );
        return newContent;
    }    
}

function convertURLs( assetInstances, mode ) {
    console.log("convertURLs " + mode );
    for( id in assetInstances ) {
        console.log("Upadting id " + id);
        var el = document.getElementById( id );
        if ( el != null ) {
            console.log("el " + el );
            var asset = assetInstances[ id ];
            var newContent = asset.updateAsset( id, mode );
            el.innerHTML = newContent;
        }
    }
}
