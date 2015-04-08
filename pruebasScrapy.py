# coding: utf-8
#-*- encoding utf-8 -*-
from bs4 import *
import urllib2
import re
import requests
import evento


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
search = "bigdata"
print "BUSQUEDA: ", search
payload = {'q': search, 'year': 't'}
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
	print "###############################################################################################"
	#	print site+a.get('href')

	# Ir a Evento y cargar
	#a = "http://www.wikicfp.com//cfp/servlet/event.showcfp?eventid=43581&copyownerid=74425"
	#ua = "Mozilla/9.0 (compatible; Konqueror/3.5.8; Linux)"  
	#headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:37.0) Gecko/20100101 Firefox/37.0', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"'}
	
	#h = {"User-Agent": headers}  
	#r = urllib2.Request(a, headers=headers)  
	#f = urllib2.urlopen(r)  
	#print a #url evento wikiCFP
	#r = requests.get(site+a.get('href'))
	#http://www.wikicfp.com/cfp/servlet/event.showcfp?eventid=41503
	#payload = {'eventid':41503}
	#st = "http://www.wikicfp.com/cfp/servlet/event.showcfp"
	print site+a.get('href')
	r = requests.get(site+a.get('href'))
	soup = BeautifulSoup(r.text)
	
	print "abriendo...."
	f=open("untitled.html","w")
	print "escribiendo...."
	f.write(soup.encode('utf-8'))
	f.close()
	print "guardado"

	# Nombre del evento
	eventName = soup.find("div", class_="contsec").find("h2").span.select('span[property="v:description"]')[0].string # div h2 span span.string
	print "** NOMBRE EVENTO: ", eventName

	# Url del evento (externo WIKICFP)
	urlEvent = soup.find("div", class_="contsec").table.tr.find_next_sibling("tr").find_next_sibling("tr").a.get('href')
	print "** URL EVENTO: ", urlEvent
	
	# Fechas del Evento
	dateEvent = soup.find("div", class_="contsec").table.tr.find_next_sibling("tr").find_next_sibling("tr")
	dateEvent = dateEvent.find_next_sibling("tr").find_next_sibling("tr").table.table.find(text="When")
	dateEvent = dateEvent.find_parent("tr").td.string
	print "** FECHAS DEL EVENTO: ", dateEvent

	# Lugar del evento
	whereEvent = soup.find("div", class_="contsec").table.tr.find_next_sibling("tr").find_next_sibling("tr")
	whereEvent = whereEvent.find_next_sibling("tr").find_next_sibling("tr").table.table.find(text="Where")
	whereEvent = whereEvent.find_parent("tr").td.string
	print "** LUGAR EVENTO: ", whereEvent

	# Abstract Registration del evento
	abstractRegist = soup.find("div", class_="contsec").table.tr.find_next_sibling("tr").find_next_sibling("tr")
	abstractRegist = abstractRegist.find_next_sibling("tr").find_next_sibling("tr").table.table.find(text="Abstract Registration Due")	
	if abstractRegist == None: 
		print "NO abstractRegist"
	else:
		abstractRegist = abstractRegist.find_parent("tr").td.select('span[property="v:startDate"]')[0].string
		print "** REGISTRO ABSTRACT DUE: ", abstractRegist

	# Submission Deadline del evento
	submissionDeadline = soup.find("div", class_="contsec").table.tr.find_next_sibling("tr").find_next_sibling("tr")
	submissionDeadline = submissionDeadline.find_next_sibling("tr").find_next_sibling("tr").table.table.find(text="Submission Deadline")
	
	if submissionDeadline == None: 
		print "NO submissionDeadline"
	else:
		submissionDeadline = submissionDeadline.find_parent("tr").td.select('span[property="v:startDate"]')[0].string
		print "** FECHA LIMITE: ", submissionDeadline

	# Notification Due del evento
	notificationDue = soup.find("div", class_="contsec").table.tr.find_next_sibling("tr").find_next_sibling("tr")
	notificationDue = notificationDue.find_next_sibling("tr").find_next_sibling("tr").table.table.find(text="Notification Due")
	
	if notificationDue == None: 
		print "NO notificationDue"
	else:
		notificationDue = notificationDue.find_parent("tr").td.select('span[property="v:startDate"]')[0].string
		print "** NOTIFICACION LIMITE: ", notificationDue

	# Final Version  Due del evento
	finalVersion = soup.find("div", class_="contsec").table.tr.find_next_sibling("tr").find_next_sibling("tr")
	finalVersion = finalVersion.find_next_sibling("tr").find_next_sibling("tr").table.table.find(text="Final Version Due")
	
	if finalVersion == None: 
		print "NO finalVersion"
	else:
		finalVersion = finalVersion.find_parent("tr").td.select('span[property="v:startDate"]')[0].string
		print "** VERSION FINAL: ", finalVersion

	#Abstract Registration Due	Jun 2, 2015
	#Submission Deadline	Jun 9, 2015
	#Notification Due	Jul 14, 2015
	#Final Version Due	Aug 10, 2015

	# CATEGORIAS
	categ = soup.find_all("table", class_="gglu")[1].h5
	print categ


	# Topics
	topicsEvent_estruct = BeautifulSoup(soup.find("div", class_="cfp").prettify())
	topicsEvent = ""
	for  txt in topicsEvent_estruct.stripped_strings:
		topicsEvent = topicsEvent +'\n'+ txt
	print topicsEvent
	#break
	
	
#print matchedCategorias
#print r.text