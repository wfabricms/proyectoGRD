from bs4 import *
import urllib2
import re
import requests

#http://www.scimagojr.com/journalsearch.php?q=2157-6904&tip=iss
#fil = ['http://www.scimagojr.com/journalsearch.php?q=14879&tip=sid&clean=0','http://www.scimagojr.com/journalsearch.php?q=19700190323&tip=sid&clean=0','http://www.scimagojr.com/journalsearch.php?q=22882&tip=sid&clean=0']
#payload = {'header1$txtSearch':'web','header1$Button1':'Search','rbSortOrder':'CID','side1$txtCalendar':''} #header1%24txtSearch=web&header1%24Button1=Search&rbSortOrder=CID&side1%24txtCalendar=
#r = requests.get("http://www.cfplist.com", params=payload)
cont = 0
fil = open("linksWOSSearchinScimago.txt")

def extraerName(soup):
	journalName = soup.find_all('h1', class_='menor')[1].string
	return journalName

def extraerCoutry(soup):
	journalCountry = soup.find(text="Country").find_parent("p").a.string
	return journalCountry

def extraerAreas(soup):
	subjectArea = soup.find(text="Subject Area").find_parent("p").find_all('a')
	subjectList = []
	if subjectArea != None:
		for tagA in subjectArea:
			subjectList.append(tagA.string)
	else:
		return None
	return subjectList

def extraerPublisher(soup):
	publisher = soup.find('strong', text="Publisher").find_parent("p").a.string
	return publisher

def extraerISSN(soup):
	ISSN = soup.find('strong', text="ISSN").find_next_sibling(text=True)
	return ISSN

def extraerCoverage(soup):
	coverage = soup.find('strong', text="Coverage:").find_next_sibling(text=True)
	return coverage

def extraerHIndex():
	hIndex = soup.find('strong', text="H Indexa").find_next_sibling(text=True)
	return hIndex

def extraerSubjecCat(soup):
	SubjectCategory = soup.find('strong', text="Subject Category").find_parent("p")
	if SubjectCategory.table == None:
		SubjectCategory = SubjectCategory.a.string
	else:
		yearsTagTh = SubjectCategory.table.thead.tr.find_next_sibling('tr').find_all('th')
		years = ["c"]
		tablaQ = []
		for th in yearsTagTh:
			years.append(th.string)
		
		tablaQ.append(years)

		subjectTagA = SubjectCategory.table.tbody.tr.find_all('a')
		for a in subjectTagA:
			SubjectCatFil = []
			SubjectCatFil.append(a.string)
			td = a.find_parent('td')
			td = td.find_next_sibling('td')
			while td!= None:
				if td.find('img') != None:
					SubjectCatFil.append(td.img.get('title'))
				else:
					SubjectCatFil.append("")
				td = td.find_next_sibling('td')
			tablaQ.append(SubjectCatFil)


		for f in tablaQ[1:]:
			indicef = 0
			for c in f[1:]:
				if c != "":
					print f[0], " - ",c, " - ",tablaQ[0][indicef]
				indicef = indicef + 1

	
for link in fil:
	if cont == 5: break
	r = requests.get(link)

	print r.url
	soup = BeautifulSoup(r.text)
	soup = soup.find(id='derecha_contenido')
	
	name = extraerName(soup)
	print name
	
	country = extraerCoutry(soup)
	print "JOURNAL COUNTRY: ", country
	"""			
	print "SUBJECT AREA: ", subjectArea

	print "PUBLISHER: ", publisher
	
	print "ISSN: ", ISSN
	"""
	
	cont = cont +1
	print "############################################################################################################"
fil.close()	