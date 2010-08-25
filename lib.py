#!/usr/bin/env python2.5

HEADERS = {
	'Host': 'portal.yzu.edu.tw',
	'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; zh-TW; rv:1.9.0.1) Gecko/2008070206 Firefox/3.0.1',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'zh-tw,en-us;q=0.7,en;q=0.3',
	'Accept-Encoding': 'gzip,deflate',
	'Accept-Charset': 'Big5,utf-8;q=0.7,*;q=0.7',
	'Keep-Alive': '300 ',
	'Connection': 'keep-alive'
}

urlNEWS = '/VC/board/showboard.asp%s'
urlHW = '/VC/Homework/FNewWorklist.asp%s'
urlSCORE = '/VC/score/detailscr.asp%s'

def injection(arg):
	if arg.find("|") >= 0:
		return True
	if arg.find(";") >= 0:
		return True
	if arg.find(">") >= 0:
		return True
	if arg.find("<") >= 0:
		return True
	if arg.find("'") >= 0:
		return True
	if arg.find('"') >= 0:
		return True
	if arg.find(")") >= 0:
		return True
	if arg.find("(") >= 0:
		return True
	if arg.find("$") >= 0:
		return True
	if arg.find("-") >= 0:
		return True
	if arg.find("[") >= 0:
		return True
	if arg.find("]") >= 0:
		return True
	if arg.find("{") >= 0:
		return True
	if arg.find("}") >= 0:
		return True
	if arg.find(":") >= 0:
		return True
	if arg.find("?") >= 0:
		return True
	if arg.find(".") >= 0:
		return True
	if arg.find(",") >= 0:
		return True
	if arg.find("~") >= 0:
		return True
	if arg.find("`") >= 0:
		return True
	
	return False

