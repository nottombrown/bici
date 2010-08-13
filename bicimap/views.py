from django.http import HttpResponse
from django.shortcuts import render_to_response
from settings import MEDIA_URL
from django.core import serializers
from bicimap.kiosks.models import Kiosk
from bicimap.kiosks.models import Record
import datetime

# Create your views here.
def index(request):
    """Render the map"""
    return render_to_response('map.html', {'MEDIA_URL': MEDIA_URL, "kiosk_data": kiosk_data})
    
def kiosk_data(request):
    """Give a snapshot of the current kiosk data"""
    json_serializer = serializers.get_serializer("json")()
    data = json_serializer.serialize(Kiosk.objects.all()) #stream=response, ensure_ascii=False
    return HttpResponse(data, mimetype='application/json')
    
def hour_interval_recs(kiosk_id):
    """Returns the 24 hour history with the most recent records at the end"""
    kiosk = Kiosk.objects.get(number=kiosk_id)
    #return the most recent 24 Records (most recent at front)
    recs = Record.objects.filter(kiosk=kiosk).order_by('-date')[:24*6:6] 
    
    # most recent are now at the end
    return recs[::-1]
    
def today_recs(request,kiosk_id):
    """Return the hour interval history of the kiosk from the day"""
    
    recs = hour_interval_recs(kiosk_id)
    # reorder them to start at midnight
    today = datetime.date.today();

    today_recs = []
    for rec in recs:
        if (rec.date.date() == today):
            today_recs.append(rec)

    json_serializer = serializers.get_serializer("json")()
    history = json_serializer.serialize(today_recs)
    return HttpResponse(history, mimetype='application/json')
    
def today_predictions(request,kiosk_id):
    """Predict the remaining hour intervals of the day"""
    # For now we just use yesterday.
    recs = hour_interval_recs(kiosk_id)
    # reorder them to start at midnight
    today = datetime.date.today();

    yesterday_recs = []
    for rec in recs:
        if (rec.date.date() != today):
           yesterday_recs.append(rec)

    json_serializer = serializers.get_serializer("json")()
    history = json_serializer.serialize(yesterday_recs)
    return HttpResponse(history, mimetype='application/json')

