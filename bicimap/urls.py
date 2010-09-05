from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('bicimap.views',
    # Example:
    # (r'^bici/', include('bici.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
     (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),
     (r'^$', 'index'),
      (r'^en$', 'index_en'),
     (r'^kiosk_data$', 'kiosk_data'),
     (r'^today_predictions/(?P<kiosk_id>\d+)/$', 'today_predictions'),
     (r'^today_recs/(?P<kiosk_id>\d+)/$', 'today_recs'),
)
