# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2018-05-25 11:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('image', models.ImageField(blank=True, upload_to='business_images')),
                ('location', models.CharField(max_length=30)),
                ('additional_details', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Neighborhood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('location', models.CharField(max_length=100)),
                ('population', models.CharField(max_length=128)),
                ('police', models.CharField(max_length=12)),
                ('ambulance', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_post', models.ImageField(blank=True, upload_to='uploaded_images')),
                ('image_details', models.CharField(max_length=1000)),
                ('text_post', models.CharField(max_length=1000)),
            ],
        ),
    ]
