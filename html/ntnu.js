function updateAsset( id, asset, mode ) {
    newContent = "";
    if ( mode == "local" ) {
        newContent = "<img id=\"img-" + id + "\" src=\"" + asset[2] + "\"/>";
    } else if ( mode == "url" ) {
        newContent = "<img id=\"img-" + id + "\" src=\"" + asset[1] + "\"/>";
    }
    console.log("updateAsset(" + id + "," + asset + "," + mode + ") =>" + newContent );
    return newContent;
}

function convertURLs( assets, mode ) {
    console.log("convertURLs " + mode );
    for( id in assets ) {
        console.log("Upadting id " + id);
        el = document.getElementById( id );
        if ( el != null ) {
            console.log("el " + el );
            asset = assets[ id ];
            newContent = updateAsset( id, asset, mode );
            el.innerHTML = newContent;
        }
    }
}
