#!/usr/bin/env python2.5
# -*- coding: utf8 -*-


import httplib, datetime, string, sys
sys.path.append('/home/college/95/s951533/.python')
import PyRSS2Gen
from BeautifulSoup import BeautifulSoup

headers = {
	'Host': 'cad_contest.ee.ntu.edu.tw',
	'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; zh-TW; rv:1.9.0.1) Gecko/2008070206 Firefox/3.0.1',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'zh-tw,en-us;q=0.7,en;q=0.3',
	'Accept-Encoding': 'gzip,deflate',
	'Accept-Charset': 'Big5,utf-8;q=0.7,*;q=0.7',
	'Keep-Alive': '300 ',
	'Connection': 'keep-alive',
	'Content-type' :'application/x-www-form-urlencoded'
}
conn = httplib.HTTPConnection('140.112.42.200')
conn.request('GET', '/cad09/news.htm', {}, headers)
soup = BeautifulSoup(conn.getresponse().read())
conn.close()

tt = string.maketrans("年月日\n", "//////////")
tn = string.maketrans("\n\r\t", "   ")
RSSitems = []
rows = soup.findAll('tr')
for row in rows[2:]:
	cells = ["".join(x.findAll(text=True)).encode('utf8') for x in row.findAll('td')]
	cells[1] =  cells[1].translate(tt).split('/')
	cells[1] = [int(x) for x in (cells[1][2], cells[1][5], cells[1][8])]
	RSSitems.append(PyRSS2Gen.RSSItem(
		title = "/".join(str(x) for x in cells[1]),
		author = '',
		categories = '',
		link = "http://140.112.42.200/cad09/news.htm",
		description =  cells[2].translate(tn).decode('utf8'), 
		guid = PyRSS2Gen.Guid("/".join(str(x) for x in cells[1])),
		pubDate = datetime.datetime(cells[1][0], cells[1][1], cells[1][2], 0, 0)
	))
rss = PyRSS2Gen.RSS2(
	title = "News Update for IC CAD Contest 2009",
	link = "http://140.112.42.200/cad09/news.htm",
	description = "News Update for IC CAD Contest 2009",
	lastBuildDate = datetime.datetime.now(),
	items = RSSitems
)

print rss.to_xml()

