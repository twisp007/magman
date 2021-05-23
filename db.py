import os
from pprint import pprint

import sqlite3

mlinks_table = 'mlinks'

mlinks_db = 'mlinks'

db_path = None
def connect(db_name):
    global db_path
    db_path = 'database/' + db_name + '.sqlite'

    try:
        db_is_new = not os.path.exists(db_path)

        if db_is_new:
            print('INFO : Creating Database for the first time...')
            with sqlite3.connect(db_path) as conn:
                schema_filename = 'database/schema.sql'
                with open(schema_filename, 'rt') as f:
                    schema = f.read()
                    conn.executescript(schema)
    except Exception as e:
        db_path = None
        print('error establishing db connection : ', e)


def addLink(dataDict, retrieved = False):
    connect(mlinks_db)
    infohash = dataDict['infohash']
    magnetLink = dataDict['magnet']
    title = dataDict['title']
    uploader = dataDict['uploader']
    size = int(dataDict['size'])
    seeds = int(dataDict['seeds'])
    peers = int(dataDict['peers'])
    verified = dataDict['verified']
    source = dataDict['source']
    if db_path is None:
        print("ERROR : DB : addLink: ", 'db_path is None')
        exit()

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        try:
            #insert into submissions_table
            query = "INSERT INTO " + mlinks_table + " (infohash, magnetLink, title, uploader, size, seeds, peers, verified, source, retrieved) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(query, (infohash, magnetLink, title, uploader, size, seeds, peers, verified, source, retrieved))

        except sqlite3.IntegrityError:
            print('ERROR: ID (infohash) already exists in PRIMARY KEY column : ', infohash)

        else:
            print("Added New DB Entry: ")
            pprint(dataDict)

def updateLink(data):
    connect(mlinks_db)
    infohash = data['infohash']
    columns = ['magnetLink', 'title', 'uploader', 'size', 'seeds', 'peers', 'verified', 'source', 'retrieved']

    if db_path is None:
        print("ERROR : DB : updateLink: ", 'db_path is None')
        exit()

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            for column in columns:
                if column in data:
                    query = "UPDATE " + mlinks_table + " SET " + column + " = ? WHERE infohash = ?"
                    cursor.execute(query, (data[column], infohash))

    except Exception as e:
        print("ERROR: Failed to update MLINKS table : " , e)

def removeLink(infohash):
    connect(mlinks_db)
    if db_path is None:
        print("ERROR : DB : removeLink: ", 'db_path is None')
        exit()

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            query = "DELETE FROM " + mlinks_table + " WHERE infohash = ?"
            cursor.execute(query, (infohash,))
    except Exception as e:
        print("ERROR: Failed to delete in DOMAINS TABLE : " , e)

def getNewMagnetLinks():
    connect(mlinks_db)

    newMagnetLinks = []

    if db_path is None:
        print("ERROR : DB : getNewMagnetLinks: ", 'db_path is None')
        exit()

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        query = "SELECT infohash, magnetLink, title, uploader, size, seeds, peers, verified, source FROM " + mlinks_table + " WHERE retrieved = ?"
        cursor.execute(query, ('0'))

        for row in cursor.fetchall():
            infohash = row[0]
            magnetLink = row[1]
            title = row[2]
            uploader = row[3]
            size = row[4]
            seeds = row[5]
            peers = row[6]
            verified = row[7]
            source = row[8]
            newMagnetLinks.append(
                {
                    'title' : title,
                    'magnetLink' : magnetLink,
                    'infohash' : infohash,
                    'uploader' : uploader,
                    'size' : size,
                    'seeds' : seeds,
                    'peers' : peers,
                    'verified' : verified,
                    'source' : source
                }
            )

        for item in newMagnetLinks:
            updatedData = {
                'infohash' : item['infohash'],
                'retrieved' : True
            }
            updateLink(updatedData)

    return newMagnetLinks
