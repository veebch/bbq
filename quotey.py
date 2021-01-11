
from time import sleep
import argparse
from PIL import Image, ImageDraw, ImageFont
from sys import path
from IT8951 import constants
import os, random
import textwrap
import qrcode


def print_system_info(display):
    epd = display.epd

    print('System info:')
    print('  display size: {}x{}'.format(epd.width, epd.height))
    print('  img buffer address: {:X}'.format(epd.img_buf_address))
    print('  firmware version: {}'.format(epd.firmware_version))
    print('  LUT version: {}'.format(epd.lut_version))
    print()

def _place_text(img, text, x_offset=0, y_offset=0):
    '''
    Put some centered text at a location on the image.
    '''
    fontsize = 350

    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype('./fonts/JosefinSans-Light.ttf', fontsize)
    except OSError:
        font = ImageFont.truetype('/usr/share/fonts/TTF/DejaVuSans.ttf', fontsize)

    img_width, img_height = img.size
    text_width, _ = font.getsize(text)
    text_height = fontsize

    draw_x = (img_width - text_width)//2 + x_offset
    draw_y = (img_height - text_height)//2 + y_offset

    draw.text((draw_x, draw_y), text, font=font,fill=(0,0,0) )

def clear_display(display):
    print('Clearing display...')
    display.clear()

def newyorkercartoon():
    print("Get a Cartoon")

def guardianheadlines():
    print("Get the Headlines")

def wordaday():
    print("get word a day")

def socialmetrics():
    print("get social metrics")

def redditquotes():
    print("get reddit quotes")

def display_image_8bpp(display):
    gudepath = 	"gudetama.png"
    # clearing image to white
    clear_display(display)
#    display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))
    
    img = Image.new("RGB", (1448, 1072), color = (255, 255, 255) )
    imggude = Image.open(gudepath)
    # TODO: this should be built-in
    dims = (display.width, display.height)

    img.thumbnail(dims)
    paste_coords = [dims[i] - img.size[i] for i in (0,1)]  # align image with bottom of display

    imggude2=imggude.resize((700,500), Image.ANTIALIAS)
    img.paste(imggude2,(450, 250))
    sleep(1)
    _place_text(img,"$34,150",0,350)
    img=img.rotate(180, expand=True)
    display.frame_buf.paste(img, paste_coords)

    display.draw_full(constants.DisplayModes.GC16)


def parse_args():
    p = argparse.ArgumentParser(description='Test EPD functionality')
    p.add_argument('-v', '--virtual', action='store_true',
                   help='display using a Tkinter window instead of the '
                        'actual e-paper device (for testing without a '
                        'physical device)')
    p.add_argument('-r', '--rotate', default=None, choices=['CW', 'CCW', 'flip'],
                   help='run the tests with the display rotated by the specified value')
    return p.parse_args()

def main():

    args = parse_args()

    tests = []

    if not args.virtual:
        from IT8951.display import AutoEPDDisplay

        print('Initializing EPD...')

        # here, spi_hz controls the rate of data transfer to the device, so a higher
        # value means faster display refreshes. the documentation for the IT8951 device
        # says the max is 24 MHz (24000000), but my device seems to still work as high as
        # 80 MHz (80000000)
        display = AutoEPDDisplay(vcom=-2.69, rotate=args.rotate, spi_hz=24000000)

        print('VCOM set to', display.epd.get_vcom())

#        tests += [print_system_info]

    else:
        from IT8951.display import VirtualEPDDisplay
        display = VirtualEPDDisplay(dims=(800, 600), rotate=args.rotate)
    print_system_info(display)
    my_list = [guardianheadlines, wordaday, redditquotes,socialmetrics,newyorkercartoon]
    random.choice(my_list)()
    display_image_8bpp(display)
    print('Done!')

if __name__ == '__main__':
    main()
