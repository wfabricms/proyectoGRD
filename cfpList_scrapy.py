# coding: utf-8
#-*- encoding utf-8 -*-
from bs4 import *
import urllib2
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
payload = {'header1$txtSearch':'web','header1$Button1':'Search','rbSortOrder':'CID','side1$txtCalendar':''} #header1%24txtSearch=web&header1%24Button1=Search&rbSortOrder=CID&side1%24txtCalendar=
r = requests.head("http://www.cfplist.com", params=payload)
print r
print r.url
#soup = BeautifulSoup(r.text)
#print soup
print "abriendo...."
f=open("untitled.html","w")
print "escribiendo...."
f.write(r.text.encode('utf-8'))
f.close()
print "guardado"


