#!/usr/local/env python2.5
# -*- coding: utf8 -*-

from sys import path
path.append('/home/college/95/s951533/.python')
import xlrd

def testXLSparser(file):
	book = xlrd.open_workbook(file).sheet_by_index(0)
# 0:系所名稱 1:年級 2:課號 3:班別 4:課名 5:授課老師 
# 6:人數 7:考試日期　8:考試時間 9:考試教室 10:備註

	dict = {}
	for _row_idx in range(book.nrows)[1:] :
		_row = book.row(_row_idx)
		_key = _row[2].value + _row[3].value
		dict[_key] = [x.value for x in _row]
	
	return dict

def parse_row(row):
	try:
		date = int(float(row[7]))
		year = date/10000
		date -= (year*10000)
		month = date/100
		date -= month*100
		year += 1911
	except:
		year = date = month = -1

	for _idx in range(len(row)):
		_entry = row[_idx]
		if type(_entry) == type(1) or type(_entry) == type(1.0):
			row[_idx] = str(_entry)
#	data =  '課名: %s(%s%s)\n' % (row[4].encode('utf8'), row[2].encode('utf8'), row[3].encode('utf8'))
	data =  ''
	if year == 2008:
		data += '考試時間: %s/%s/%s %s\n' % (year, month, date, row[8].encode('utf8'))
	else:
		data += '考試時間: %s %s\n' % (row[7].encode('utf8'), row[8].encode('utf8'))
	data += '考試教室: %s\n' % row[9].encode('utf8')
	data += '備註: %s\n' % row[10].encode('utf8')
	return data
