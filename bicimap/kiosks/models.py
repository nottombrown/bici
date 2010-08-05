from django.db import models

# Create your models here.
class Kiosk(models.Model):
	name = models.CharField(max_length=200)
	last_updated = models.DateTimeField('last updated')
	lat = models.FloatField()
	lng = models.FloatField()
	spaces = models.IntegerField()
	bikes = models.IntegerField()
	
	def __unicode__(self):
		return self.name
		
	