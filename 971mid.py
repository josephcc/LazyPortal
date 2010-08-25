#!/usr/bin/env python2.5
# -*- coding: utf8 -*-

from sys import argv, path, exit, stderr
path.append('/home/college/95/s951533/.python')
from operator import itemgetter
from lib import *
from parser import * 
import os
import PyRSS2Gen
import datetime

from libportal import get_cookie
from interface import get_class_list

USER = argv[1] 
PSWD = argv[2]
if not(injection(USER)) :
	os.system("/usr/bin/touch /home/college/95/s951533/portal/users/971mid/%s" % USER)

cookie = get_cookie(USER, PSWD)
class_list = get_class_list(cookie)
print >> stderr, class_list
class_list = [x[0] for x in class_list]
print >> stderr, class_list

dict = testXLSparser('/home/college/95/s951533/portal/target.xls')

data = []
for _key in class_list:
	print >> stderr, _key
	try:
		data.append(dict[_key])
	except:
		data.append(['', '', _key,'' , '', '', '', '', '', '', u'查無資料'])
	
# 0:系所名稱 1:年級 2:課號 3:班別 4:課名 5:授課老師 
# 6:人數 7:考試日期　8:考試時間 9:考試教室 10:備註
data = sorted(data, key=itemgetter(7), reverse = False)

RSSitems = []
for _row in data :
	_desc = parse_row(_row).decode('utf8')
	try:
		date = int(float(_row[7].encode('utf8')))
	except:
		date = 890101
	year = date/10000
	date -= (year*10000)
	month = date/100
	date -= month*100
	RSSitems.append(PyRSS2Gen.RSSItem(
		title = ("[%s] %s by %s" % (_row[2]+_row[3], _row[4], _row[5])),
		author = _row[5],
		link = "http://www.yzu.edu.tw",
		categories = _row[5],
		description = _desc,
		guid = PyRSS2Gen.Guid(_desc),
		pubDate = datetime.datetime(year+1911,month,date,0, 0, 0)
	))

rss = PyRSS2Gen.RSS2(
	title = "Portal News for %s" % USER,
	link = "https://portal.yzu.edu.tw/",
	description = "The latest news or your portal",
	lastBuildDate = datetime.datetime.now(),
	items = RSSitems,
	image = PyRSS2Gen.Image("http://moon.cse.yzu.edu.tw/~s951533/portal/exam.jpg",
		"exam", "https://portal.yzu.edu.tw")
)

print rss.to_xml()

