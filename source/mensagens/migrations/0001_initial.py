# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-18 14:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('anuncio', models.CharField(max_length=140, unique=True, verbose_name='Anúncio')),
                ('mensagem', models.TextField(max_length=5000)),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('updates', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Anúncio',
                'verbose_name_plural': 'Anúncios',
                'ordering': ['-timestamp', '-updates'],
            },
        ),
    ]
