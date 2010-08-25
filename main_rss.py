#!/usr/bin/env python2.5
# -*- coding: utf8 -*-
from sys import argv, path
path.append('/home/college/95/s951533/.python')

import psyco
psyco.full()

import PyRSS2Gen
from lib import *
import os
import datetime

from libportal import get_cookie
from interface import *

# input id paswd
USER = argv[1] 
PSWD = argv[2]

if not(injection(USER)) :
	os.system("/usr/bin/touch /home/college/95/s951533/portal/users/news/%s" % USER)

cookie = get_cookie(USER, PSWD)
class_list = get_class_list(cookie)
news = get_news(cookie, class_list)

date, author, info, link, class_name = range(5)

RSSitems = []
for new in news :
	_date = [int(x) for x in new[date].split('/')]
	RSSitems.append(PyRSS2Gen.RSSItem(
		title = ("[%s]%s by %s" % (new[date].encode('utf8'), new[class_name], new[author])).decode('utf8').strip(),
		author = new[author].decode('utf8').strip(),
		link = "https://portal.yzu.edu.tw/",
		description = ' '.join(new[info].splitlines()).decode('utf8').strip(), 
		pubDate = datetime.datetime(_date[0], _date[1], _date[2], 0, 0)
	))
rss = PyRSS2Gen.RSS2(
	title = "Portal News for %s" % USER,
	link = "https://portal.yzu.edu.tw/",
	description = "The latest news or your portal",
	lastBuildDate = datetime.datetime.now(),
	items = RSSitems,
	image = PyRSS2Gen.Image("http://moon.cse.yzu.edu.tw/~s951533/portal/yzu.png",
		"python", "http://www.yzu.edu.tw/")
)

print rss.to_xml()

