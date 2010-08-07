# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Kiosk'
        db.create_table('kiosks_kiosk', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('full_address', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lng', self.gf('django.db.models.fields.FloatField')()),
            ('spaces', self.gf('django.db.models.fields.IntegerField')()),
            ('bikes', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('kiosks', ['Kiosk'])


    def backwards(self, orm):
        
        # Deleting model 'Kiosk'
        db.delete_table('kiosks_kiosk')


    models = {
        'kiosks.kiosk': {
            'Meta': {'object_name': 'Kiosk'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'bikes': ('django.db.models.fields.IntegerField', [], {}),
            'full_address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lng': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'spaces': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['kiosks']
