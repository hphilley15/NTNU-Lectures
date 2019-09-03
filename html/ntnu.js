class JBData {
    typeEnum = {
        JBDATA : 0,
        JBIMAGE : 1,
        JBVIDEO: 2,    
    };
    constructor( name, url=None, data=None, localFile=None, type = typeEnum.JBDATA, suffix=".dat" ) {
        this.type = typeEnum.JBDATA;
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

class JBImage extends JBData {
    constructor( name, width, height, url=None, data=None, localFile=None ) {
        super( name, url, data, localFile, JBata.typeEnum.JBIMAGE, "png");
        this.width = width;
        this.height = height;
        console.log("JBImage(" + name + "," + url + "," + localFile + ")" );
    }

    updateAsset( id, mode ) {
        newContent = "";
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
        super( name, url, data, localFile, JBata.typeEnum.JBVIDEO, "mp4");
        this.width = width;
        this.height = height;
        console.log("JBVideo(" + name + "," + url + "," + localFile + ")" );
    }

    updateAsset( id, mode ) {
        newContent = "";
        if ( mode == "local" ) {
            newContent = "<img id=\"img-" + id + "\" src=\"" + this.localFile + "\"/>";
        } else if ( mode == "url" ) {
            newContent = "<img id=\"img-" + id + "\" src=\"" + this.url + "\"/>";
        }
        console.log("JBVideo.updateAsset(" + id + "," + "," + mode + ") =>" + newContent );
        return newContent;
    }    
}

function convertURLs( assets, mode ) {
    console.log("convertURLs " + mode );
    for( id in assets ) {
        console.log("Upadting id " + id);
        el = document.getElementById( id );
        if ( el != null ) {
            console.log("el " + el );
            asset = assets[ id ];
            newContent = asset.updateAsset( id, mode );
            el.innerHTML = newContent;
        }
    }
}
