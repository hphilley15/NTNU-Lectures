import sys
from PyTexturePacker import Packer
from plistlib import load 
import re

def packCharacters( src, dest ):
    packer = Packer.create(max_width=2048, max_height=2048, shape_padding=4, trim_mode=1, reduce_border_artifacts=True, bg_color=0xffffff00)
    packer.pack( src, dest )

def nameToFields( fname ):
    p = re.compile(r'^\W*(?P<name>[A-Za-z0-9]+)[\W_]+(?P<obj>[A-Za-z0-9]+)[\W_]*(?P<tags>[^.]*)[.](png|jpg|jpeg)$')
    p = re.compile(r'^\W*(?P<name>[A-Za-z0-9]+)[\W_]+(?P<obj>[A-Za-z0-9]+)[\W_]*(?P<tags>[^.]*)[.](png|jpg|jpeg)$')
    m = p.match( fname )

#    print("Trying to match", fname)
    if m:
#        print("Match found fname", fname, "name", m.group('name'), "obj", m.group('obj'), "tags", m.group('tags')  )
        if m.group('name'):
            name = m.group('name').lower()
        else:
            name = "NAMEERROR"

        if m.group('obj'):
            obj = m.group('obj').lower()
        else:
            obj = "OBJERROR"

        if m.group('tags'):
            sp = re.compile(r'\W+')
            tags = sp.split( m.group( 'tags' ).lower() )
            #print('tags', tags)
        else:
            tags = []
        
        result =  ( name, obj, tags )
    else:
        result = None
    return result

def appendToCSS( pFile, rdir ):
    with open(pFile, "rb") as f:
        pd = load( f )

    frames = pd['frames']
    md = pd['metadata']

    #res = nameToFields('jacky-leftarm-up-down.jpeg')
    #res = nameToFields(' ProfJB_Head.png')
    css = ""
    html = ""

    for f in frames:
        print("Frame", f )
        res = nameToFields( f )
        print('res', res )
        print("rotated", frames[f]['rotated'] )

        id = res[0] + "_" + res[1]
        for t in res[2]:
            id = id + "_" + t
        print('id', id)
        print(frames[f])
        coords = re.compile(r' *{ *{ *(?P<px>[0-9.]+) *, *(?P<py>[0-9.]+) *} *, *{ *(?P<width>[0-9.]+) *, *(?P<height>[0-9.]+) *} *}')
        m = coords.match(frames[f]['frame'] )
        if m:
            px = int( m.group('px') )
            py = int( m.group('py') )
            width = int( m.group('width') )
            height = int( m.group('height') )
            print('texture', px, py, width, height )


        srect = re.compile(r' *{ *{ *(?P<sx>[0-9.]+) *, *(?P<sy>[0-9.]+) *} *, *{ *(?P<width>[0-9.]+) *, *(?P<height>[0-9.]+) *} *}')
        m = srect.match(frames[f]['sourceColorRect'] )
        if m:
            sx = int( m.group('sx') )
            sy = int( m.group('sy') )
            swidth = int( m.group('width') )
            sheight = int( m.group('height') )
            print('source rect', sx, sy, swidth, sheight )

            fileName = rdir + "/" + md['textureFileName']
            if frames[f]['rotated']:
                rot = " rotate(-90deg)"
                width,height = height,width
            else:
                rot = ""

            cssRec = f"""
#{id} {{
  width: {width}px;
  height: {height}px;
  position: absolute;
  background: url("{fileName}") -{px}px -{py}px;
  transform: translate({sx}px, {sy}px){rot};
}}
"""
            print(cssRec)
            css = css + cssRec

            ctags = " ".join(res[2])
            htmlRec = f"""
<div id="{id}" class="{ctags}" style="visibility:hidden"></div>
"""
            html = html + htmlRec
    return css, html, None
    
def main( argv = None ):
    if argv is None:
        argv = sys.argv[1:]
    #packCharacters( argv[0], argv[1] )
    css = ""
    html = ""

    cs, ht, js = appendToCSS("prof_jb_0.plist", "../assets")
    css = css + cs
    html = html + ht
    cs, ht, js = appendToCSS("prof_jb_1.plist", "../assets")
    css = css + cs
    html = html + ht
    #css = css + appendToCSS("prof_jb_2.plist", "../assets")

    with open('prof_jb.css','w') as f:
        f.write(css)

    with open('prof_jb.html','w') as f:
        f.write(html)

if __name__ == "__main__":
    main( [ '../../Lecture-VN/Resources/ProfJB/', "prof_jb_%d"] )
