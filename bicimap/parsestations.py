#!/usr/local/bin/python
# coding: utf-8
from elementtree import ElementTree
import datetime
import os
from django.core.management import setup_environ
import settings
# first set up django env
setup_environ(settings)
# then import kiosk information
from kiosks.models import Kiosk

# information is from http://www.sevici.es/service/carto
def initialize_kiosks():
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
		k = Kiosk(number=number,name=name,address=address,full_address=full_address,lat=lat,lng=lng,last_updated=datetime.datetime.now())
		k.save()
	
# detail infor from http://www.sevici.es/service/stationdetails/%s
def update_kiosk_details(num):
	output_file = "crawler/details"+str(num)
	os.system("wget http://www.sevici.es/service/stationdetails/" + str(num) + " -O "+ output_file)
	tree = ElementTree.parse(output_file)
	kiosk_elt = tree.getroot()
	avail_elt = kiosk_elt.find("available")
	bikes = int(avail_elt.text)
	spaces = int(kiosk_elt.find("free").text)
	# total = int(kiosk_elt.find("total").text)
	
	kiosk = Kiosk.objects.get(number=num)
	kiosk.bikes = bikes
	kiosk.spaces = spaces
	kiosk.save()
	

def update_all_kiosks():
	for k in Kiosk.objects.all():
		update_kiosk_details(k.number)
	