#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import feedparser
import requests
import os
import logging

from logging.handlers import TimedRotatingFileHandler
from pprint import pprint

from dotenv import load_dotenv
load_dotenv()

logname = "check_manga.log"
handler = TimedRotatingFileHandler(logname, when="midnight", interval=1)
handler.suffix = "%Y%m%d"
logger = logging.getLogger('simple')
logger.addHandler(handler)

logging.basicConfig(level="INFO")

discordUrl = os.environ.get("url")
list_manga = os.environ.get("list_manga").split("|")
flux_rss = os.environ.get("flux_rss")

news_feed = feedparser.parse(flux_rss)

news = []

check_manga = open("check_manga.log", "r")
with open('check_manga.log') as f:
    lines = f.read().splitlines()

check_manga.close()

for entry in news_feed.entries:
    if entry.link not in lines:
        print(entry.link)
        if any("/"+ext+"/" in entry.link for ext in list_manga):
            r = requests.get(entry.link)
            if "SPOILER" in r.text or "Version VUS" in r.text or "RAW" in r.text:
                continue
            logger.info(entry.link)
            news.append(entry.link)

if len(news) > 0:
    response = requests.post(discordUrl, data={"content": "@everyone "+', '.join(news)})

logging.shutdown()
