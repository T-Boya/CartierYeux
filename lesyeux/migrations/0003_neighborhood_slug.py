# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2018-05-26 12:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesyeux', '0002_auto_20180526_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='neighborhood',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]