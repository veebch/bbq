#!/usr/bin/python3
import requests
import urllib, json
from PIL import Image, ImageOps
from PIL import ImageFont
from PIL import ImageDraw
import yaml
import json
import logging
import os

configfile = os.path.join(os.path.dirname(os.path.realpath(__file__)),'config.yaml')


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
        print(quotestack[0].encode("utf-8"))
    except:
        print('Reddit Does Not Like You')

if __name__ == '__main__':
    main()