from django.http import HttpResponse
from django.shortcuts import render_to_response
from settings import MEDIA_URL
from django.core import serializers
from bicimap.kiosks.models import Kiosk
from bicimap.kiosks.models import Record

# Create your views here.
def index(request):
  return render_to_response('map.html', {'MEDIA_URL': MEDIA_URL, "kiosk_data": kiosk_data})
  
def kiosk_data(request):
  json_serializer = serializers.get_serializer("json")()
  kiosk_data = json_serializer.serialize(Kiosk.objects.all()) #stream=response, ensure_ascii=False
  return HttpResponse(kiosk_data, mimetype='application/json')
  
def kiosk_history(request,kiosk_id):
  kiosk = Kiosk.objects.get(number=kiosk_id)
  json_serializer = serializers.get_serializer("json")()
  #return the most recent 24 Records
  recent_records = Record.objects.filter(kiosk=kiosk).order_by('date')[:24]
  kiosk_history = json_serializer.serialize(recent_records)
  return HttpResponse(kiosk_history, mimetype='application/json')