# flake8: noqa
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DummyModel'
        db.create_table('user_tags_dummymodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('user_tags', ['DummyModel'])

        # Adding model 'TaggedItem'
        db.create_table('user_tags_taggeditem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('user_tags', ['TaggedItem'])

        # Adding M2M table for field user_tag on 'TaggedItem'
        db.create_table('user_tags_taggeditem_user_tag', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('taggeditem', models.ForeignKey(orm['user_tags.taggeditem'], null=False)),
            ('usertag', models.ForeignKey(orm['user_tags.usertag'], null=False))
        ))
        db.create_unique('user_tags_taggeditem_user_tag', ['taggeditem_id', 'usertag_id'])

        # Adding model 'UserTag'
        db.create_table('user_tags_usertag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_tag_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['user_tags.UserTagGroup'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('user_tags', ['UserTag'])

        # Adding unique constraint on 'UserTag', fields ['user_tag_group', 'text']
        db.create_unique('user_tags_usertag', ['user_tag_group_id', 'text'])

        # Adding model 'UserTagGroup'
        db.create_table('user_tags_usertaggroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('user_tags', ['UserTagGroup'])

    def backwards(self, orm):
        # Removing unique constraint on 'UserTag', fields ['user_tag_group', 'text']
        db.delete_unique('user_tags_usertag', ['user_tag_group_id', 'text'])

        # Deleting model 'DummyModel'
        db.delete_table('user_tags_dummymodel')

        # Deleting model 'TaggedItem'
        db.delete_table('user_tags_taggeditem')

        # Removing M2M table for field user_tag on 'TaggedItem'
        db.delete_table('user_tags_taggeditem_user_tag')

        # Deleting model 'UserTag'
        db.delete_table('user_tags_usertag')

        # Deleting model 'UserTagGroup'
        db.delete_table('user_tags_usertaggroup')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'user_tags.dummymodel': {
            'Meta': {'object_name': 'DummyModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'user_tags.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user_tag': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['user_tags.UserTag']", 'symmetrical': 'False'})
        },
        'user_tags.usertag': {
            'Meta': {'unique_together': "(('user_tag_group', 'text'),)", 'object_name': 'UserTag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'user_tag_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['user_tags.UserTagGroup']"})
        },
        'user_tags.usertaggroup': {
            'Meta': {'object_name': 'UserTagGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['user_tags']
