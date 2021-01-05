#!/usr/bin/python3
import requests
import urllib, json
from PIL import Image, ImageOps
from PIL import ImageFont
from PIL import ImageDraw
from waveshare_epd import epd2in7
import yaml
import json
import logging
import os
import re
import sys
import unicodedata
import time


configfile = os.path.join(os.path.dirname(os.path.realpath(__file__)),'config.yaml')

def beanaproblem():
#   A visual cue that the wheels have fallen off
    thebean = Image.open(os.path.join(picdir,'thebean.bmp'))
    epd = epd2in7.EPD()
    epd.Init_4Gray()
    image = Image.new('L', (epd.height, epd.width), 255)    # 255: clear the image with white
    draw = ImageDraw.Draw(image)
    image.paste(thebean, (60,15))
    image = ImageOps.mirror(image)
    epd.display_4Gray(epd.getbuffer_4Gray(image))
    epd.sleep()
    epd2in7.epdconfig.module_exit()

def main():
    quoteurl = 'https://www.reddit.com/r/quotes/top/.json?t=week'
    with open(configfile) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    logging.info(config)
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
        print(result.decode())
        i+=1

if __name__ == '__main__':
    main()