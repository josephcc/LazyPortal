#!/usr/bin/env python2.5
# -*- coding: utf8 -*-

import libportal
import time

def _date_cmp(unformated_date):
	date_set = [int(x) for x in unformated_date.split('/')] 
	return date_set

def get_class_list(cookie):
	return libportal.get_class_list(cookie)

def get_class_news(cookie, class_set):
	print libportal.get_class_news(cookie, class_set[2])

def get_class_homework(cookie, class_set):
	return libportal.get_class_homework(cookie, class_set[2])

def get_news(cookie, class_list):
	allnews = []
	for x in class_list:
		news =  libportal.get_class_news(cookie, x[2])
		news = [list(n) for n in news]
		news = [n + [x[1],] for n in news]
		allnews += news

	allnews.sort(key=lambda x: _date_cmp(x[0]), reverse=True)
	return allnews

def get_homework(cookie, class_list):
	allhomework = []
	for x in class_list:
		homework = libportal.get_class_homework(cookie, x[2])
		homework = [list(n) for n in homework]
		homework = [n + [x[1],] for n in homework]
		allhomework += homework

	allhomework.append(['/'.join([str(x) for x in time.gmtime()[0:3]]), ' - YA_AY 今天在這裡 YA_AY', '-'*100, '', '', '', ''])
	allhomework.sort(key=lambda x: _date_cmp(x[0]), reverse=True)
	return allhomework

def get_links(cookie, class_set):
	class_link = class_set[2]
	links = libportal.get_class_material_links(cookie, class_link)
	return links


