# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-19 14:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lares', '0003_remove_imovel_visita_fotografica'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imovelphotos',
            options={},
        ),
        migrations.RemoveField(
            model_name='imovelphotos',
            name='order',
        ),
    ]