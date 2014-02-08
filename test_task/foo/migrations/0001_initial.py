# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Users'
        db.create_table(u'foo_users', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('paycheck', self.gf('django.db.models.fields.IntegerField')()),
            ('date_joined', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'foo', ['Users'])

        # Adding model 'Rooms'
        db.create_table(u'foo_rooms', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('spots', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'foo', ['Rooms'])


    def backwards(self, orm):
        # Deleting model 'Users'
        db.delete_table(u'foo_users')

        # Deleting model 'Rooms'
        db.delete_table(u'foo_rooms')


    models = {
        u'foo.rooms': {
            'Meta': {'object_name': 'Rooms'},
            'department': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'spots': ('django.db.models.fields.IntegerField', [], {})
        },
        u'foo.users': {
            'Meta': {'object_name': 'Users'},
            'date_joined': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'paycheck': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['foo']