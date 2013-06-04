# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Email.mime_payload'
        db.add_column(u'ui_email', 'mime_payload',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Email.mime_payload'
        db.delete_column(u'ui_email', 'mime_payload')


    models = {
        u'ui.email': {
            'Meta': {'object_name': 'Email'},
            'address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_payload': ('django.db.models.fields.TextField', [], {}),
            'return_date': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['ui']