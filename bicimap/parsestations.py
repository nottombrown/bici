#!/usr/local/bin/python
# coding: utf-8
from elementtree import ElementTree
import datetime
from django.core.management import setup_environ
import settings
# first set up django env
setup_environ(settings)
# then import kiosk information
from kiosks.models import Kiosk

# information is from http://www.sevici.es/service/carto
def initialize_kioks():
	# parse tree and add to database
	tree = ElementTree.parse("crawler/stations")
	root = tree.getroot()
	
	for child in root.find("markers").findall("marker"):
		number = child.get("number")
		name = child.get("name")
		address = child.get("address")
		full_address = child.get("fullAddress")
		lat = child.get("lat")
		lng = child.get("lng")
		print name
		k = Kiosk(number=number,name=name,address=address,full_address=full_address,lat=lat,lng=lng,last_updated=datetime.datetime.now())
		k.save()
	
# detail infor from http://www.sevici.es/service/stationdetails/%s
def update_kiosk_details(num):
	os.system("wget http://www.sevici.es/service/stationdetails/" + number)

# update_kiosk_details(5)
	