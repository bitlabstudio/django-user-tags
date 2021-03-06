# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-14 15:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TaggedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_tags_tagged_items', to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='UserTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=256, verbose_name='Text')),
            ],
        ),
        migrations.CreateModel(
            name='UserTagGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.AddField(
            model_name='usertag',
            name='user_tag_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_tags.UserTagGroup', verbose_name='User tag group'),
        ),
        migrations.AddField(
            model_name='taggeditem',
            name='user_tags',
            field=models.ManyToManyField(to='user_tags.UserTag', verbose_name='User tag'),
        ),
        migrations.AlterUniqueTogether(
            name='usertaggroup',
            unique_together=set([('user', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='usertag',
            unique_together=set([('user_tag_group', 'text')]),
        ),
    ]
