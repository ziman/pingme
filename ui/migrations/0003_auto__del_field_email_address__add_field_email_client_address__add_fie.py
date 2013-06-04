# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Email.address'
        db.delete_column(u'ui_email', 'address')

        # Adding field 'Email.client_address'
        db.add_column(u'ui_email', 'client_address',
                      self.gf('django.db.models.fields.EmailField')(default='', max_length=75),
                      keep_default=False)

        # Adding field 'Email.server_address'
        db.add_column(u'ui_email', 'server_address',
                      self.gf('django.db.models.fields.EmailField')(default='', max_length=75),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Email.address'
        raise RuntimeError("Cannot reverse this migration. 'Email.address' and its values cannot be restored.")
        # Deleting field 'Email.client_address'
        db.delete_column(u'ui_email', 'client_address')

        # Deleting field 'Email.server_address'
        db.delete_column(u'ui_email', 'server_address')


    models = {
        u'ui.email': {
            'Meta': {'object_name': 'Email'},
            'client_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_payload': ('django.db.models.fields.TextField', [], {}),
            'return_date': ('django.db.models.fields.DateTimeField', [], {}),
            'server_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'})
        }
    }

    complete_apps = ['ui']