from bs4 import *
import urllib2
import re
import requests

#http://www.scimagojr.com/journalsearch.php?q=2157-6904&tip=iss
#links = ['http://www.scimagojr.com/journalsearch.php?q=2157-6904&tip=iss']
#payload = {'header1$txtSearch':'web','header1$Button1':'Search','rbSortOrder':'CID','side1$txtCalendar':''} #header1%24txtSearch=web&header1%24Button1=Search&rbSortOrder=CID&side1%24txtCalendar=
#r = requests.get("http://www.cfplist.com", params=payload)
cont = 0
fil = open("linksWOSSearchinScimago.txt")
for link in fil:
	
	if cont == 5: break
	r = requests.get(link)

	print r.url
	soup = BeautifulSoup(r.text)
	soup = soup.find(id='derecha_contenido')

	journalName = soup.find_all('h1', class_='menor')[1].string
	print "JOURNAL NOMBRE: ", journalName

	journalCountry = soup.find(text="Country").find_parent("p").a.string
	print "JOURNAL COUNTRY: ", journalCountry

	subjectArea = soup.find(text="Subject Area").find_parent("p").find_all('a')
	print "SUBJECT AREA: ", subjectArea

	publisher = soup.find('strong', text="Publisher").find_parent("p").a.string
	print "PUBLISHER: ", publisher

	ISSN = soup.find('strong', text="ISSN").find_next_sibling(text=True)
	print "ISSN: ", ISSN

	cont = cont +1
	print "############################################################################################################"
fil.close()
