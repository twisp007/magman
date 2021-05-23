import re
from time import strftime, localtime
from pprint import pprint

import db

from feedgen.feed import FeedGenerator

magnetLinks = db.getNewMagnetLinks()

fg = FeedGenerator()
fg.title('RSS for tpb')
fg.description('RSS for tpb')
fg.link(href='localhost', rel='self')

fg.load_extension('torrent')

for torrent in magnetLinks:
    #pprint(torrent)
    if torrent['verified'] == '0':
        verified = "False"
    else:
        verified = "True"
    fe = fg.add_entry()
    fe.title(torrent['title'])
    fe.content(torrent['magnetLink'])
    fe.author(name=torrent['uploader'])
    fe.link(href=torrent['magnetLink'], rel='alternate', type='application/x-bittorrent, length=1000')
    fe.torrent.infohash(torrent['infohash'])
    fe.torrent.contentlength(str(torrent['size']))
    fe.torrent.seeds(str(torrent['seeds']))
    fe.torrent.peers(str(torrent['peers']))
    fe.torrent.verified(verified)

    #size
    size_desc = None
    size = float(torrent['size'])
    if size >= 1024 * 1024 * 1024 * 1024:
        size_desc = str(round(size / 1024 / 1024 / 1024 / 1024, 2)) + " TB"
    elif size >= 1024 * 1024 * 1024:
        size_desc = str(round(size / 1024 / 1024 / 1024, 2)) + " GB"
    elif size >= 1024 * 1024:
        size_desc = str(round(size / 1024 / 1024, 2)) + " MB"
    elif size >= 1024:
        size_desc = str(round(size / 1024, 2)) + " KB"
    else:
        size_desc = torrent['size']

    #time
    currentTime = strftime("%Y-%m-%d %H:%M:%S", localtime())


    description = ("Seeds: {}, Peers: {}\nSize: {}\nHash: {}\nUpdated: {}".format(torrent['seeds'], torrent['peers'], size_desc, torrent['infohash'], currentTime))

    fe.description(description)

fg.rss_file('feed/rss.xml')
