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
	urlEvent = soup.table.tr.find_next_sibling("tr").find_next_sibling("tr").a
	if urlEvent == None:
		return None
	else:
		return urlEvent.get('href')

def comprobarTextExist(soup, search):
	dateEvent = soup.table.find("table", class_="gglu").find(text=search)
	#dateEvent = dateEvent.find_parent("tr").td.string
	return dateEvent

def estrucutrarDate(dateString):
	dateString = dateString.split()
	"""print dateString
				print dateString[2]
				print dateString[0]
				print dateString[1][:-1]"""
	return dateString[2] + '-' + mapearMes(dateString[0]) +'-'+ dateString[1][:-1]


def extraerDates(soup, search):
	dates = comprobarTextExist(soup, search)
	dates = dates.find_parent("tr").td.string
	if 'N/A' in dates or dates == None:
		return (None,None)
	else:
		dates = dates.split()
		whenBegin = dates[2] + '-' + mapearMes(dates[0]) +'-'+ dates[1][:-1]
		whenEnd   = dates[6] + '-' + mapearMes(dates[4]) +'-'+ dates[5][:-1]
		return (whenBegin,whenEnd)

def extraerWhere(soup, search):
	where = comprobarTextExist(soup, search)
	where = where.find_parent("tr").td.string
	if 'N/A' in where or where == None:
		return None
	else:
		return where

def extraerImportantDates(soup, search):
	abstractRegist = comprobarTextExist(soup, search)
	if abstractRegist == None:
		return None
	else:
		abstractRegist = abstractRegist.find_parent("tr").td.select('span[property="v:startDate"]')[0].string
		return estrucutrarDate(abstractRegist)

def extraerCateg(soup):
	categorias = soup.find_all("table", class_="gglu")[1].h5
	if categorias == None:
		return None
	else:
		categorias = categorias.find_all('a')
		categ = []
		for cat in categorias[1:]:
			categ.append(cat.string)
		return categ

def extraerDecrip(soup):
	topicsEvent_estruct = BeautifulSoup(soup.find("div", class_="cfp").prettify())
	topicsEvent = ""
	for  txt in topicsEvent_estruct.stripped_strings:
		topicsEvent = topicsEvent +'\n'+ txt
	return topicsEvent


a = "http://www.wikicfp.com/cfp/servlet/event.showcfp?eventid=45369&copyownerid=60222"
r = requests.get(a)
soup = BeautifulSoup(r.text)
soup = soup.find("div", class_="contsec")

event = Evento()

event.name = extraerName(soup)

event.url = extraerUrl(soup)

when = extraerDates(soup, "When") #return ('value1','value2')
event.whenBegin = when[0]
event.whenEnd   = when[1]

event.where = extraerWhere(soup, "Where")

event.abstractRegistration = extraerImportantDates(soup, "Abstract Registration Due")

event.submissionDeadline = extraerImportantDates(soup, "Submission Deadline") #Notification Due inal Version Due

event.notificationDue = extraerImportantDates(soup, "Notification Due")

event.finalVersionDue = extraerImportantDates(soup, "Final Version Due")

event.categories = extraerCateg(soup)

event.description = extraerDecrip(soup)

print "NOMBRE: ", event.name
print "URL: ", event.url
print "BEGIN: ", event.whenBegin
print "END: ", event.whenEnd
print "LUGAR: ", event.where
print "ABSTRACT REGIS: ", event.abstractRegistration
print "SUBMISION DEADLINE: ", event.submissionDeadline
print "NOTIFICATION DUE: ", event.notificationDue 
print "FINAL VERSION: ", event.finalVersionDue
print "CATEGORIAS: ", event.categories
print "DESCRIPTION: ",  event.description 