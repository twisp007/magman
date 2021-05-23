import json
import re
import os
from pprint import pprint

import db

def insertDB(jsonData):
    for item in jsonData:
        try:
            magnet = item['magnetLink']
        except Exception as e:
            print("ERR : json2db : unable get data from the json file: ", e)
            pprint(item)
            continue

        title = item['title']
        uploader = item['uploader']
        size = float(item['size'])
        sizeUnit = item['sizeUnit']
        seeds = int(item['seeds'])
        peers = int(item['peers'])
        verified = item['verified']
        source = item['source']

        # size

        if sizeUnit == 'TiB':
            size = size * 1099511627800
        elif sizeUnit == 'GiB':
            size = size * 1073741824
        elif sizeUnit == 'MiB':
            size = size * 1048576
        elif sizeUnit == 'KiB':
            size = size * 1024
        elif sizeUnit == 'B':
            size = size

        # verified
        if verified == "False":
            verified = False
        else:
            verified = True

        # infohash
        infohash = None
        pattern = '(?!magnet\:\?xt\=urn\:btih\:)[a-zA-Z0-9]{1,}(?=\&dn)'
        patternMatch = re.findall(pattern, magnet)
        if len(patternMatch) >= 1:
            infohash = patternMatch[0]

        magnetLink = {
            'title': title,
            'magnet': magnet,
            'infohash': infohash,
            'uploader': uploader,
            'size': size,
            'seeds': seeds,
            'peers': peers,
            'verified': verified,
            'source': source
        }

        try:
            db.addLink(magnetLink)
        except Exception as e:
            print("ERR: json2db : cannot insert magnetLink into database: ", e)
            pprint(magnetLink)


jsonData = None

fileList = os.listdir('json/')

for item in fileList:
    if item.split('.')[-1] == 'json':
        with open('json/' + item, 'r') as jsonFile:
            jsonData = json.load(jsonFile)
            insertDB(jsonData)
