from django.http import HttpResponse
from django.shortcuts import render_to_response
from settings import MEDIA_URL
from django.core import serializers
from bicimap.kiosks.models import Kiosk

# Create your views here.
def index(request):
  return render_to_response('map.html', {'MEDIA_URL': MEDIA_URL, "kiosk_data": kiosk_data})
  
def kiosk_data(request):
  json_serializer = serializers.get_serializer("json")()
  kiosk_data = json_serializer.serialize(Kiosk.objects.all()) #stream=response, ensure_ascii=False
  return HttpResponse(kiosk_data, mimetype='application/json')