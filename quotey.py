
from time import sleep
import argparse
from PIL import Image, ImageDraw, ImageFont
from sys import path
from IT8951 import constants
import os, random
import textwrap
import qrcode
import feedparser
import requests
import textwrap
import unicodedata
import re
import logging

def print_system_info(display):
    epd = display.epd

    print('System info:')
    print('  display size: {}x{}'.format(epd.width, epd.height))
    print('  img buffer address: {:X}'.format(epd.img_buf_address))
    print('  firmware version: {}'.format(epd.firmware_version))
    print('  LUT version: {}'.format(epd.lut_version))
    print()

def _place_text(img, text, x_offset=0, y_offset=0,fontsize=40):
    '''
    Put some centered text at a location on the image.
    '''

    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype('./fonts/JosefinSans-.ttf', fontsize)
    except OSError:
        font = ImageFont.truetype('/usr/share/fonts/TTF/DejaVuSans.ttf', fontsize)

    img_width, img_height = img.size
    text_width, _ = font.getsize(text)
    text_height = fontsize

    draw_x = (img_width - text_width)//2 + x_offset
    draw_y = (img_height - text_height)//2 + y_offset

    draw.text((draw_x, draw_y), text, font=font,fill=(0,0,0) )

def writewrappedlines(img,text,fontsize,y_text=-300,height=110, width=27):
    lines = textwrap.wrap(text, width)
    for line in lines:
        width= 0
        _place_text(img, line,0, y_text, fontsize)
        y_text += height
    return img

def clear_display(display):
    print('Clearing display...')
    display.clear()

def newyorkercartoon(img):
    print("Get a Cartoon")
    d = feedparser.parse('https://www.newyorker.com/feed/cartoons/daily-cartoon')
    caption=d.entries[8].summary
    imagedeets = d.entries[8].media_thumbnail[0]
    imframe = Image.open(requests.get(imagedeets['url'], stream=True).raw)
    size = 1100,1100
    imframe.thumbnail(size)
    xvalue= int(1448/2-550)
    img.paste(imframe,(xvalue, 10))

    writewrappedlines(img,caption,40,360,50,50)
    return img

def guardianheadlines(img):
    print("Get the Headlines")

    d = feedparser.parse('https://www.theguardian.com/uk/rss')
    logourl=d['feed']['image']['href']
    print(d.url)
    imlogo = Image.open(requests.get(logourl, stream=True).raw)
    img.paste(imlogo,(100, 100))


    text=d.entries[0].title
    img=writewrappedlines(img,text,80)

    return img

def nth_repl(s, sub, repl, n):
    find = s.find(sub)
    # If find is not -1 we have found at least one match for the substring
    i = find != -1
    # loop util we find the nth or we find no match
    while find != -1 and i != n:
        # find + 1 means we start searching from after the last match
        find = s.find(sub, find + 1)
        i += 1
    # If i is equal to n we found nth match so replace
    if i == n:
        return s[:find] + repl + s[find+len(sub):]
    return s

def by_size(words, size):
    return [word for word in words if len(word) <= size]

def wordaday(img):
    print("get word a day")
    return img

def socialmetrics(img):
    print("get social metrics")
    return img

def redditquotes(img):
    print("get reddit quotes")
    quoteurl = 'https://www.reddit.com/r/quotes/top/.json?t=week&limit=100'
    rawquotes = requests.get(quoteurl,headers={'User-agent': 'Chrome'}).json()
    quotestack = []
    i=0
    try:
        length= len(rawquotes['data']['children'])
        while i < length:
            quotestack.append(str(rawquotes['data']['children'][i]['data']['title']))
            i+=1
        for key in rawquotes.keys():
            print(key)
    except:
        print('Reddit Does Not Like You')

#   Tidy quotes
    i=0
    while i<len(quotestack):
        result = unicodedata.normalize('NFKD', quotestack[i]).encode('ascii', 'ignore')
        quotestack[i]=result.decode()
        i+=1
    quotestack = by_size(quotestack, 140)
    
    while True:
        quote=random.choice (quotestack)
    #   Replace rancypants quotes with vanilla quotes
        quote=re.sub("“", "\"", quote)
        quote=re.sub("”", "\"", quote)
        string = quote
        count = quote.count("\"")
        print("Count="+str(count))
        if count >= 2:
            print("2 or more quotes - split after last one")
            sub = "\""
            wanted = "\" ~"
            n = count
            quote=nth_repl(quote, sub, wanted, n)
            print(quote)

        quote= re.sub("\s+\"\s+", "\"", quote)
        quote= re.sub("~|-|—|―", "--", quote)


        splitquote = quote.split("--")
        quote = splitquote[0]

        quote = quote.strip()
        quote = quote.strip("\"")
        quote = quote.strip()

        if splitquote[-1]!=splitquote[0]:
            img=writewrappedlines(img,quote,80)
            source = splitquote[-1]
            source = source.strip()
            print(source)
            _place_text(img,source,0,380,50)
            break

    return img

def display_image_8bpp(display, img):

    dims = (display.width, display.height)
    img.thumbnail(dims)
    paste_coords = [dims[i] - img.size[i] for i in (0,1)]  # align image with bottom of display
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

    else:
        from IT8951.display import VirtualEPDDisplay
        display = VirtualEPDDisplay(dims=(800, 600), rotate=args.rotate)
    print_system_info(display)
    my_list = [newyorkercartoon]
    clear_display(display)
    img = Image.new("RGB", (1448, 1072), color = (255, 255, 255) )
    img=random.choice(my_list)(img)
    display_image_8bpp(display,img)
    print('Done!')

if __name__ == '__main__':
    main()
