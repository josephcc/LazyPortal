#!/usr/bin/env python2.5
# -*- coding: utf8 -*-

from sys import argv, path, stderr
path.append('/home/college/95/s951533/.python')
import httplib, urllib, re
from BeautifulSoup import BeautifulSoup

headers = {
	'Host': 'portal.yzu.edu.tw',
	'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; zh-TW; rv:1.9.0.1) Gecko/2008070206 Firefox/3.0.1',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'zh-tw,en-us;q=0.7,en;q=0.3',
	'Accept-Encoding': 'gzip,deflate',
	'Accept-Charset': 'Big5,utf-8;q=0.7,*;q=0.7',
	'Keep-Alive': '300 ',
	'Connection': 'keep-alive',
	'Content-type' :'application/x-www-form-urlencoded', 
}

def get_cookie(USER, PSWD):
	params = urllib.urlencode({'uid' : USER, 'pwd' : PSWD})
	conn = httplib.HTTPSConnection('portal.yzu.edu.tw')
	conn.request('POST', '/logincheck_new.asp', params, headers)
	response = conn.getresponse()
	cookie = response.getheader('set-cookie')
	cookie = cookie[:cookie.find(';')]
	conn.close()
	headers['Cookie'] = cookie

	conn.request('GET', '/Left_index.asp', {}, headers)
	response = conn.getresponse()
	response = response.read()
	response = response.decode('big5-hkscs').encode('utf8')
	conn.close()
	try:
		VClink = re.search(r'/VC2/Login_student.aspx\?[^"]*', response).group(0)
	except:
		return 'LOGIN FAILED'

	conn.request('GET', VClink, {}, headers)
	response = conn.getresponse()
	cookie = response.getheader('set-cookie')
	cookie = cookie[:cookie.find(';')]
	conn.close()
	return cookie

def get_class_list(cookie):
	headers['Cookie'] = cookie
	conn = httplib.HTTPSConnection('portal.yzu.edu.tw')
	conn.request('GET', '/VC2/Student/classLeft_S.aspx', {}, headers)
	response = conn.getresponse()
	response = response.read()
	conn.close()
	soup = BeautifulSoup(response)

	Classes = soup.findAll('a', {'class': 'left_menu'})
	print >> stderr, "# of 'a class=left_menu'", len(Classes) 

	names =  [x['title'].splitlines()[1][5:-1] for x in Classes if 'CosFrame_S' in x['href']]
	print >> stderr, "# of names", len(names)
	names = [x.encode('utf8') for x in names]

	class_link_base = '/VC2/Student/%s'
	links =  [class_link_base % x['href'] for x in Classes if 'CosFrame_S' in x['href']]
	print >> stderr, "# of links", len(links)
	links = [x.encode('utf8') for x in links]

	ids = [str(x.string) for x in Classes]
	ids = filter(lambda x: x[0].isupper() , ids )
	print >> stderr, "# of ids", len(ids)
	print >> stderr, ids
	ids = [x for x in ids]

	return [(ids[x], names[x], links[x]) for x in range(min(len(ids), len(names), len(links)))]

def _get_class_conn(cookie, class_link):
	headers['Cookie'] = cookie
	conn = httplib.HTTPSConnection('portal.yzu.edu.tw')

	conn.request('GET', class_link, {}, headers)
	response = conn.getresponse()
	response.read()
	return conn

def get_class_news(cookie, classlink):
	conn = _get_class_conn(cookie, classlink)
	conn.request('GET', '/VC2/Student/board/showboard_S.aspx', {}, headers)
	response = conn.getresponse()
	response = response.read()
	conn.close()
	soup = BeautifulSoup(response)

	Table = soup.findAll('td', {'class': 'cont'})[0].findAll('table')[1].findAll('tr')[4:-1]
	Table = [Table[x] for x in range(0, len(Table), 2)]

	info = []
	for row in Table:
		row = row.findAll('td')
		if '尚無最新消息' in str(row):
			return []

		data = '\n'.join(row[2].findAll(text=True))
		data = data.strip().encode('utf8')

		date = row[0].string.strip()
		who  = row[4].string.strip().encode('utf8')
		link = str(row[3].a)
		link = link.splitlines()
		link = ' '.join(link)
		
		info.append( (date, who, data, link) )
	
	return info

def get_class_homework(cookie, classlink):
	conn = _get_class_conn(cookie, classlink)
	conn.request('GET', '/VC2/Student/Homework/HomeWork_S.aspx', {}, headers)
	response = conn.getresponse()
	response = response.read()
	conn.close()
	soup = BeautifulSoup(response)


	soup = soup.findAll('td', {'class' : 'cont'})[0]
	soup = soup.findAll('tr')[3:-17]

	allhw = []
	for idx in range(0, len(soup), 2):
		hw = soup[idx].findAll('td')
		_number, _cat, _name, _file, _date, _upload, _btn, _score, _comment = range(9)

		date	= ''.join( hw[_date].findAll(text=True) ).strip().encode('utf8')
		name	= ''.join( hw[_name].findAll(text=True) ).strip().encode('utf8')
		cat		= ''.join( hw[_cat].findAll(text=True)).strip().encode('utf8')
		upload	= ''.join( hw[_upload].findAll(text=True) ).strip().encode('utf8')
		score	= ''.join( hw[_score].findAll(text=True) ).strip().encode('utf8')
		comment	= ''.join( hw[_comment].findAll(text=True) ).strip().encode('utf8')
		file	= hw[_file] #''.join( hw[_file].findAll(text=True) ).strip().encode('utf8')

		content	= soup[idx+1].findAll(text=True)
		content = '\n'.join(content).strip().encode('utf8')

		allhw.append((date, name, content, upload, score, comment))

	allhw = filter(lambda x: '系所評鑑/IEET' not in ''.join(x), allhw)

	return allhw

def download_class_material(cookie, filelink):
	headers['Cookie'] = cookie
	conn = httplib.HTTPSConnection('portal.yzu.edu.tw')
	conn.request('GET', '/VC2/Student/Homework/%s' % filelink, {}, headers)
	response = conn.getresponse()
	if response.getheader('content-disposition') == None:
		return
	filename = response.getheader('content-disposition')
	filename = filename[filename.find('=')+1:]
	print filename

	fp = open(filename, 'wb')
	while True:
		try:
			fp.write(response.read(1024))
		except:
			break

	fp.close()

def get_class_material_links(cookie, classlink):
	conn = _get_class_conn(cookie, classlink)
	conn.request('GET', '/VC2/Student/Materials/Materials_S.aspx', {}, headers)
	response = conn.getresponse()
	response = response.read()
	conn.close()
	soup = BeautifulSoup(response)
	soup = soup.findAll('a')
	filelist = [x['href'] for x in soup]
	filelist = filter(lambda x: 'File_name=' in x, filelist)
	return filelist


