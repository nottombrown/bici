#!/usr/bin/python
# coding: utf-8
""" Parses information from www.sevici.es. Available commands are ["help", "init", "update"]
"""
from elementtree import ElementTree
import datetime
import os
from django.core.management import setup_environ
import sys
import getopt
import settings
# first set up django env
setup_environ(settings)
# then import kiosk information
from kiosks.models import Kiosk
from django.db import IntegrityError
from settings import ROOT_DIR


# information is from http://www.sevici.es/service/carto
def initialize_kiosks():
    # parse tree and add to database
    tree = ElementTree.parse(ROOT_DIR+ "bicimap/crawler/stations")
    root = tree.getroot()
    
    for child in root.find("markers").findall("marker"):
        number = child.get("number")
        name = child.get("name")
        address = child.get("address")
        full_address = child.get("fullAddress")
        lat = child.get("lat")
        lng = child.get("lng")
        
        #Check if it's already in the database
        try:
            kio = Kiosk(number=number,
                            name=name,
                            address=address,
                            full_address=full_address,
                            lat=lat,lng=lng,
                            last_updated=datetime.datetime.now())
            kio.save()
            print "Added kiosk number: %d" % int(number)
        except IntegrityError, msg:
            print msg

# detail information from http://www.sevici.es/service/stationdetails/%s
def update_kiosk_details(num):
    output_file = ROOT_DIR+"bicimap/crawler/details/detail"+str(num)
    os.system("wget http://www.sevici.es/service/stationdetails/" + str(num) + " -O "+ output_file)
    tree = ElementTree.parse(output_file)
    kiosk_elt = tree.getroot()
    avail_elt = kiosk_elt.find("available")
    bikes = int(avail_elt.text)
    spaces = int(kiosk_elt.find("free").text)
    # total = int(kiosk_elt.find("total").text)
    
    kiosk = Kiosk.objects.get(number=num)
    kiosk.update_status(bikes=bikes,spaces=spaces)
    kiosk.save()
    

def update_all_kiosks():
    for k in Kiosk.objects.all():
        update_kiosk_details(k.number)
        
def process(arg):
    if (arg == "init"):
        initialize_kiosks()
    elif (arg == "update"):
        update_all_kiosks()
    else:
        print __doc__ #print docstring
        sys.exit("2")

def main():
    try:
        #opts is a lists of strings, args is a list of (opt, opt_val) tuples 
        #opts were preceded by a hyphen in the command
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"]) 
    except getopt.error, msg:
        print msg
        print "for help use --help"
        return 2 #exit code 2 is a syntax error
    # process options
    for opt, opt_val in opts:
        if opt in ("-h", "--help"):
            print __doc__
            return 0 #exit code 0 means successful termination
    #process args
    for arg in args:
        process(arg)


if __name__ == "__main__":
        sys.exit(main())
