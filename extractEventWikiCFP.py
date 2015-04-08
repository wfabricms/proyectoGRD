# coding: utf-8
#-*- encoding utf-8 -*-
from bs4 import *
import urllib2
import re
import requests
from evento import Evento

def mapearMes(mes):
	mesMap = [('Jan','1'),('Feb','2'),('Mar','3'),('Apr','4'),('May','5'),('Jun','6'),('Jul','7'),('Aug','8'),('Sep','9'),('Oct','10'),('Nov','11'),('Dic','12')]
	for mesLetra, mesNum in mesMap:
		if mesLetra == mes:
			return mesNum
	return "err"


def extraerName(soup):
	eventName = soup.find("h2").span.select('span[property="v:description"]')[0].string
	return eventName

def extraerUrl(soup):	
	urlEvent = soup.table.tr.find_next_sibling("tr").find_next_sibling("tr").a.get('href')
	return urlEvent

def extraerDataTable(soup, search):
	dateEvent = soup.table.tr.find_next_sibling("tr").find_next_sibling("tr")
	dateEvent = dateEvent.find_next_sibling("tr").find_next_sibling("tr").table.table.find(text=search)
	dateEvent = dateEvent.find_parent("tr").td.string
	return dateEvent

def extraerDates(soup, search):
	dates = extraerDataTable(soup, search)
	if 'N/A' in dates or dates == None:
		return ('null','null')
	else:
		dates = dates.split()
		whenBegin = dates[2] + '-' + mapearMes(dates[0]) +'-'+ dates[1][:-1]
		whenEnd   = dates[6] + '-' + mapearMes(dates[4]) +'-'+ dates[5][:-1]
		return (whenBegin,whenEnd)

def extraerWhere(soup, search):
	where = extraerDataTable(soup, search)
	if 'N/A' in where or where == None:
		return 'null'
	else:
		return where


a = "http://www.wikicfp.com//cfp/servlet/event.showcfp?eventid=44457&copyownerid=50937"
r = requests.get(a)
soup = BeautifulSoup(r.text)
soup = soup.find("div", class_="contsec")

event = Evento()
event.name = extraerName(soup)
event.url = extraerUrl(soup)
when = extraerDates(soup, "When")
event.whenBegin = when[0]
event.whenEnd   = when[1]

event.where = extraerWhere(soup, "Where")

print event.name
print "url", event.url

print event.whenBegin
print event.whenEnd
print event.where