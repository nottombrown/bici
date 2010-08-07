from django.db import models

# Create your models here.
class Kiosk(models.Model):
  number = models.IntegerField(null=True)
  name = models.CharField(max_length=200)
  address = models.CharField(max_length=200)
  full_address = models.CharField(max_length=200)
  last_updated = models.DateTimeField('last updated')
  lat = models.FloatField()
  lng = models.FloatField()
  spaces = models.IntegerField()
  bikes = models.IntegerField()
  
  def full(self):
    return (self.spaces < 1)
    
  def empty(self):
    return (self.bikes < 1)

  def __unicode__(self):
    return self.name
    
  