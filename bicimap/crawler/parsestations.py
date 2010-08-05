#!/usr/local/bin/python
# coding: utf-8

# information is from http://www.sevici.es/service/carto
# import django
# from django.core import serializers
# import os
# # import xmltramp
# 
# stations = open("crawler/stations")
# print stations.read()
# 
# for obj in serializers.deserialize("xml", stations):
#     print obj

from xml.dom import minidom
sock = openAnything("http://www.sevici.es/service/carto")
minidom.parse(sock)
sock.close