from django.db import models
import datetime

# Create your models here.
class Kiosk(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    full_address = models.CharField(max_length=200)
    last_updated = models.DateTimeField('last updated')
    lat = models.FloatField()
    lng = models.FloatField()
    spaces = models.IntegerField(null=True)
    bikes = models.IntegerField(null=True)
    
    def full(self):
        return (self.spaces < 1)
        
    def empty(self):
        return (self.bikes < 1)

    def __unicode__(self):
        return self.name
        
    def update_status(self, bikes, spaces):
        self.bikes = bikes
        self.spaces = spaces
        #store the information as a record too
        record = Record(kiosk=self,
                                        spaces=spaces,
                                        bikes=bikes)
        record.save()
        
class Record(models.Model):
    kiosk = models.ForeignKey(Kiosk, null=True)
    date = models.DateTimeField('date fetched', auto_now=True)
    spaces = models.IntegerField()
    bikes = models.IntegerField()
    
    def __unicode__(self):
        return ("kiosk " + str(self.kiosk.number) + " updated: " + str(self.date))