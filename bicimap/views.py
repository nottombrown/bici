from django.http import HttpResponse
from django.shortcuts import render_to_response

# Create your views here.
def index(request):
		    cool_text = "this is sweet text"
		    return render_to_response('temp.html', {'sweet_text': cool_text})