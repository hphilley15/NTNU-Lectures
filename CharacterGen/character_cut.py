#!/usr/bin/env python 

from PIL import Image
import sys
import argparse
import numpy as np
import pathlib

def cropImage( fname ):
    file = pathlib.Path( fname )

    if args.verbose > 0:
        print("Auto cropping image", file)
    im = np.array( Image.open(file) )
    height, width, depth = im.shape
    if depth == 4:
        top = 0
        while( top < height ):
            if sum( im[top,:,3] ) == 0:
                top = top + 1
            else:
                break
        bottom = height
        while( bottom > 0 ):
            if sum( im[bottom-1,:,3] ) == 0:
                bottom = bottom - 1
            else:
                break
        left = 0
        while( left < width ):
            if sum( im[:,left,3] ) == 0:
                left = left + 1
            else:
                break
        right = width
        while( right > 0 ):
            if sum( im[:,right-1,3] ) == 0:
                right = right - 1
            else:
                break
        if args.verbose:
            print('ROI:', top, left, bottom, right )
        cropped = Image.fromarray( im[ top:bottom, left:right ] )
        cropped.save( "/tmp/test/{0}-{1}-{2}.png".format(top, left, file.stem ) )
        
    
args = None

def main( argv = None ):
    if not argv:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser( description="Automatically crop images")
    parser.add_argument( 'images', nargs='+', help='images' )
    parser.add_argument( '-c', '--command', default=cropImage, nargs=1, help='command')    
    parser.add_argument( '-v', '--verbose', default=0, action='count', help='verbose output')
    global args    
    args = parser.parse_args( argv )
    for f in args.images:
        args.command( f )

if __name__ == "__main__":
    main()
