# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-14 20:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lares', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='imovel',
            name='video',
            field=models.URLField(blank=True, null=True),
        ),
    ]
