# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2018-05-26 17:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lesyeux', '0005_remove_post_image_details'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='image_post',
            new_name='image',
        ),
    ]
