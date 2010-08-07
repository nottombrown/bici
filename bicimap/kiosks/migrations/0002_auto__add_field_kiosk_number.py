# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Kiosk.number'
        db.add_column('kiosks_kiosk', 'number', self.gf('django.db.models.fields.IntegerField')(null=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Kiosk.number'
        db.delete_column('kiosks_kiosk', 'number')


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
            'number': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'spaces': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['kiosks']
