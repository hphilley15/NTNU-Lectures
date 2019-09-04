#!/usr/bin/env python 

from PIL import Image
import sys
import argparse
import numpy as np
import pathlib

def loadImage( fname ):
    file = pathlib.Path( str(fname) )

    if args.verbose > 0:
        print("Loading image", file)
    im = np.array( Image.open(file) )
    return im

def saveImage( img, fname ):
    img.save( fname )
        
def trimImage( img ):
    height, width, depth = img.shape
    if depth == 4:
        top = 0
        while( top < height ):
            if sum( img[top,:,3] ) == 0:
                top = top + 1
            else:
                break
        bottom = height
        while( bottom > 0 ):
            if sum( img[bottom-1,:,3] ) == 0:
                bottom = bottom - 1
            else:
                break
        left = 0
        while( left < width ):
            if sum( img[:,left,3] ) == 0:
                left = left + 1
            else:
                break
        right = width
        while( right > 0 ):
            if sum( img[:,right-1,3] ) == 0:
                right = right - 1
            else:
                break
        if args.verbose:
            print('ROI:', top, left, bottom, right )
        cropped = cropImage( img, top, left, bottom, right )
        cropped.save( "/tmp/test/{0}-{1}-{2}.png".format(top, left, file.stem ) )

def cropImage( img, top, left, bottom, right ):
    file = pathlib.Path( fname )
    im = np.array( Image.open(file) )

    if args.verbose > 0:
        print("Cropping image", file)
   cropped = Image.fromarray( img[ top:bottom, left:right ] )
   return cropped
    
args = None

def trim( fname ):
    file = pathlib.Path( fname )
    img = loadImage( file )
    trimmed, top, left, bottom, right = trimImage( img )
    saveImage( trimmed, f"{file.stem}-{top}-{left}.png" )

def main( argv = None ):
    if not argv:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser( description="Automatically crop images")
    parser.add_argument( 'images', nargs='+', help='images' )
    parser.add_argument( '-c', '--command', default=trimImage, nargs=1, help='command')    
    parser.add_argument( '-v', '--verbose', default=0, action='count', help='verbose output')
    global args    
    args = parser.parse_args( argv )
    for f in args.images:
        eval( args.command + "(" + f + ")" )

if __name__ == "__main__":
    main()
