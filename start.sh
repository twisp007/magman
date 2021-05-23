#!/usr/bin/env bash

LOGFILE="/home/vyom/var/magman/magman.log"

echo "==================================================================" >> $LOGFILE
echo "==================================================================" >> $LOGFILE
date >> $LOGFILE

echo >> $LOGFILE

rm /home/vyom/var/magman/json/*.json
echo "removed old json files from previous crawling" >> $LOGFILE

cd //home/vyom/var/magman/magman/
scrapy crawl trntz -o /home/vyom/var/magman/json/trntz.json >> $LOGFILE
echo "crawling finished" >> $LOGFILE
scrapy crawl tpb -o /home/vyom/var/magman/json/tpb.json >> $LOGFILE
echo "crawling finished" >> $LOGFILE

cd /home/vyom/var/magman/

python /home/vyom/var/magman/json2db.py $LOGFILE
echo "info stored in db" >> magman.log

rm /home/vyom/var/magman/feed/rss.xml
echo "removed old rss feed" >> $LOGFILE

python /home/vyom/var/magman/generateFeed.py >> $LOGFILE
echo "rss feed updated" >> $LOGFILE

echo "*******************************************************************" >> $LOGFILE

exit
