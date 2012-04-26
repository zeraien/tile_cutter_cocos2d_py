#!/usr/bin/env python
# Written by Dmitri Fedortchenko / One Day Beard
#
# Use as you see fit, and attribute if you wish.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import Image
import sys
import optparse
import os

def cut_it(input_filename, output_filename, tile_width, tile_height, suffix):
    image = Image.open(input_filename)
    if not suffix: suffix = ''
    suffix = suffix.strip("\s\t\"\'\n")
    
    tiles = []
    tile_dict = {
        'filename': os.path.basename(input_filename),
        'width':image.size[0],
        'height':image.size[1],
        'tiles':tiles
    }
    
    if image.size[0] % tile_width == 0 and image.size[1] % tile_height ==0 :
        row = 0
        currentx = 0
        currenty = 0
        while currenty < image.size[1]:
            column = 0
            while currentx < image.size[0]:
                tile = image.crop((currentx,currenty,currentx + tile_width,currenty + tile_height))
                
                tile_filename = "%s_%s_%s%s.png" % (output_filename, row, column, suffix)
                tile.save(tile_filename,"PNG")
                
                tiles.append({
                    'filename':os.path.basename(tile_filename),
                    'rect':'{{%s,%s},{%s,%s}}' % (currentx,currenty,tile_width, tile_height)
                })
                
                currentx += tile_width
                column+=1
            currenty += tile_height
            currentx = 0
            row+=1
    else:
        print "sorry your image does not fit neatly into",tile_width,"*",tile_height,"tiles"
        sys.exit(1)
        
    return tile_dict
    
def make_plist(tile_dict):
    
    source_bit = """<key>Filename</key>
<string>%(filename)s</string>
<key>Size</key>
<string>{%(width)d, %(height)d}</string>
"""
    tile_bit = """<dict>
	<key>Name</key>
	<string>%(filename)s</string>
	<key>Rect</key>
	<string>%(rect)s</string>
</dict>
"""
    
    plist_structure = """<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
    	<key>Source</key>
    	<dict>%(source_bit)s</dict>
    	<key>Tiles</key>
    	<array>%(tile_bits)s</array>
    </dict>
    </plist>
"""
    source_bit = source_bit % tile_dict
    
    tile_bits = []
    for tile_data in tile_dict['tiles']:
        tile_bits.append(tile_bit % tile_data)
    plist_structure = plist_structure % {'source_bit':source_bit, 'tile_bits':''.join(tile_bits)}
    return plist_structure
    
if __name__=="__main__":
    parser = optparse.OptionParser()
    parser.usage = "usage: %prog [options]"
    
    parser.add_option("-o", "--output", dest="output_filename",
                      help="output name, sans extension (may include directory)", metavar="NAME")
    parser.add_option("-s", "--suffix", dest="suffix",
                  help="suffix for file names, such as '-hd'. Please use quotes if your suffix includes a dash.", metavar="SUFFIX")
    parser.add_option("-i", "--input", dest="input_filename",
                    help="input file", metavar="FILE")
    parser.add_option("-x", "--tileWidth", metavar="VALUE", dest="tile_width",
                      help="tile width", type="int")
    parser.add_option("-y", "--tileHeight", metavar="VALUE", dest="tile_height",
                    help="tile height", type="int")
                      
    (options, args) = parser.parse_args()
    
    if not options.input_filename:
        parser.error("no input file specified")
    if not options.output_filename:
        parser.error("no output file specified")
    if int(options.tile_height) <= 0:
        parser.error("invalid tile height %s" % options.tile_height)
    if int(options.tile_width) <= 0:
        parser.error("invalid tile width %s" % options.tile_width)
    if not os.path.exists(os.path.abspath(options.input_filename)):
        options.input_filename =  os.path.abspath(options.input_filename)
        parser.error("input file '%s' not found" % options.input_filename)

    plist_filename = '%s.plist' % options.output_filename
    if os.path.exists(os.path.abspath(plist_filename)):
        parser.error("file exists: %s" % plist_filename)
        
    tile_dict = cut_it(**options.__dict__)
    
        
    with open(plist_filename, 'w') as f:
        f.write(make_plist(tile_dict))