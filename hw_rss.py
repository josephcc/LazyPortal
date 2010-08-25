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
homeworks = get_homework(cookie, class_list)

date, title, info, upload, score, dont_know, class_name = range(7)

RSSitems = []
for hw in homeworks :
	_date = [int(x) for x in hw[date].split('/')]
	RSSitems.append(PyRSS2Gen.RSSItem(
		title = ("[%s]%s - %s" % (hw[date], hw[title], hw[class_name])).decode('utf8').strip(),
		author = hw[class_name].decode('utf8').strip(),
		link = "https://portal.yzu.edu.tw/",
		description = (' '.join(hw[info].splitlines()) + " <繳交狀況: " + hw[upload] + "> <成績: " + hw[score]+">").decode('utf8').strip(), 
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

