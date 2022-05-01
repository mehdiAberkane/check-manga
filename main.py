#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import feedparser
import requests
import os
import logging

from logging.handlers import TimedRotatingFileHandler

logname = "check_manga.log"
handler = TimedRotatingFileHandler(logname, when="midnight", interval=1)
handler.suffix = "%Y%m%d"
logger = logging.getLogger('simple')
logger.addHandler(handler)

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level="INFO")

discordUrl = os.environ.get("url")
list_manga = os.environ.get("list_manga").split("|")

news_feed = feedparser.parse('https://www.japscan.ws/rss/')

news = []

check_manga = open("check_manga.log", "r")
with open('check_manga.log') as f:
    lines = f.read().splitlines()

for entry in news_feed.entries:
    if entry.link not in lines:
        if any(ext in entry.link for ext in list_manga):
            logger.info(entry.link)
            news.append(entry.link)


if len(news) > 0:
    response = requests.post(discordUrl, data={"content": "@everyone "+', '.join(news)})
