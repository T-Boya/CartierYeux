# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2018-05-26 17:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesyeux', '0006_auto_20180526_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploaded_images'),
        ),
    ]