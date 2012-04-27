Tile Cutter
======================

Because I couldn't not get the famed https://github.com/jlamarche/Tile-Cutter and https://github.com/psineur/Tile-Cutter/network to work in Mac OS X 10.7, with PNG images,
I googled around and found a simply python implementation.

Improving upon it, and adding support for creation of cocos2d-esque plist files, here we are.

Huh?
========================

This will take an image, and cut it into a number of tiles. It will also create a plist file containing references to these tiles that can be read by CCBigImage.

More about CCBigImage here: https://github.com/cocos2d/cocos2d-iphone-extensions/tree/develop/Extensions/CCBigImage

The output will be PNG files and one plist file.

Dependencies
========================
Required python libraries: Python Image Library (aka Image, PIL).


Idea and some code was found here:http://blog.odonnell.nu/posts/creating-tiles-image-python-and-pil/

Usage
=======================

    Usage: usage: tilecut.py [options]

    Options:
      -h, --help            show this help message and exit
      -o NAME, --output=NAME
                            output name, sans extension (may include directory)
      -s SUFFIX, --suffix=SUFFIX
                            suffix for file names, such as '-hd'. Please use
                            quotes if your suffix includes a dash.
      -i FILE, --input=FILE
                            input file
      -x VALUE, --tileWidth=VALUE
                            tile width
      -y VALUE, --tileHeight=VALUE
                            tile height
### Example
    
    ../tilecut.py -i ../originals/ship_panorama-hd.png -x 424 -y 320 -o ship_panorama -s "-hd"
    

Will create the files you are looking for.



Limitations
========================
If your tiles all need to be the same size, the image has to accommodate for this, or you must choose your tile sizes accordingly.

Feel free to fork and improve!