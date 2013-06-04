# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Email'
        db.create_table(u'ui_email', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('return_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'ui', ['Email'])


    def backwards(self, orm):
        # Deleting model 'Email'
        db.delete_table(u'ui_email')


    models = {
        u'ui.email': {
            'Meta': {'object_name': 'Email'},
            'address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'return_date': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['ui']