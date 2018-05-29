# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2018-05-29 06:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lesyeux', '0013_auto_20180527_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='user_dps'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='neighborhood',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lesyeux.Neighborhood'),
        ),
    ]
