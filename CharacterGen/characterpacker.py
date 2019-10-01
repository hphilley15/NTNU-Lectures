import sys
from PyTexturePacker import Packer

def packCharacters( src, dest ):
    packer = Packer.create(max_width=2048, max_height=2048, shape_padding=2, trim_mode=1, reduce_border_artifacts=True, bg_color=0xffffff00)
    packer.pack( src, dest )

def main( argv = None ):
    if argv is None:
        argv = sys.argv[1:]
    packCharacters( argv[0], argv[1] )
    
if __name__ == "__main__":
    main( [ '../../Lecture-VN/Resources/ProfJB', "prof_jb_%d"] )
