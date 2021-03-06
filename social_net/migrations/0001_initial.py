# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-07-28 08:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_action', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=500, null=True)),
                ('publication_date', models.DateTimeField(default=datetime.datetime(2017, 7, 28, 11, 16, 50, 622016))),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user_action.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, null=True)),
                ('body', models.TextField(max_length=3000, null=True)),
                ('image', models.ImageField(null=True, upload_to='images/')),
                ('publication_date', models.DateTimeField(default=datetime.datetime(2017, 7, 28, 11, 16, 50, 620651))),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_action.Profile')),
                ('likes', models.ManyToManyField(blank=True, related_name='post_likes', to='user_action.Profile')),
            ],
            options={
                'ordering': ['-publication_date'],
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='social_net.Post'),
        ),
    ]
