# coding: utf-8
#-*- encoding utf-8 -*-
from bs4 import *
from urllib import urlopen
import re
import requests
"""	
r = requests.get('https://api.github.com/events')
print r
r = requests.post("http://httpbin.org/post")
print r
r = requests.put("http://httpbin.org/put")
print r
r = requests.delete("http://httpbin.org/delete")
print r
r = requests.head("http://httpbin.org/get")
print r
r = requests.options("http://httpbin.org/get")
print r
"""

#http://www.wikicfp.com/cfp/servlet/tool.search?q=semantic+web&year=t
payload = {'q': 'web', 'year': 't'}
r = requests.get("http://www.wikicfp.com/cfp/servlet/tool.search", params=payload)
print r
print r.url
soup = BeautifulSoup(r.text)

# Matched Categories
matchedCategorias = soup.find("div", class_="contsec").table.tr.find_next_sibling("tr").find_all("a")
for a in matchedCategorias:
	print a

# Matched Call For Papers
site = "http://www.wikicfp.com/"
matchedRst = soup.find("div", class_="contsec").table.table.find_all("a")
for a in matchedRst:
	#	print site+a.get('href')

	# Ir a Evento y cargar
	print site+a.get('href') #url evento wikiCFP
	#r = requests.get(site+a.get('href'))
	r = urlopen(site+a.get('href')).read()
	soup = BeautifulSoup(r)

	# Nombre del evento
	eventName = soup.find("div", class_="contsec").find("h2").span.select('span[property="v:description"]')[0].string # div h2 span span.string
	print eventName

	# Url del evento (externo WIKICFP)
	urlEvent = soup.find("div", class_="contsec").table.tr.find_next_sibling("tr").find_next_sibling("tr").a.get('href')
	print urlEvent
	# Fechas del Evento
	dateEvent = soup.find("div", class_="contsec").table.tr.find_next_sibling("tr").find_next_sibling("tr")
	dateEvent = dateEvent.find_next_sibling("tr").find_next_sibling("tr").table.table.find(text="When")
	dateEvent = dateEvent.find_parent("tr").td.string
	print dateEvent

	# Lugar del evento
	whereEvent = soup.find("div", class_="contsec").table.tr.find_next_sibling("tr").find_next_sibling("tr")
	whereEvent = whereEvent.find_next_sibling("tr").find_next_sibling("tr").table.table.find(text="Where")
	whereEvent = whereEvent.find_parent("tr").td.string
	print whereEvent

	# Topics
	topicsEvent = soup.select(".cfp")
	print topicsEvent
	print
	print "###############################################################################################"
	break
	
#print matchedCategorias
#print r.text