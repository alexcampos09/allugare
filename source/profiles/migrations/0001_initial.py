# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-18 14:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import profiles.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('width', models.IntegerField(blank=True, default=0, null=True)),
                ('height', models.IntegerField(blank=True, default=0, null=True)),
                ('profilePic', models.ImageField(blank=True, height_field='height', null=True, upload_to=profiles.models.upload_location, verbose_name='Foto de Perfil', width_field='width')),
                ('nome', models.CharField(blank=True, max_length=120, null=True, verbose_name='Nome completo')),
                ('universidade', models.CharField(blank=True, max_length=120, null=True)),
                ('curso', models.CharField(blank=True, max_length=120, null=True)),
                ('uf', models.CharField(blank=True, choices=[('SP', 'SP'), ('AC', 'AC'), ('AL', 'AL'), ('AM', 'AM'), ('AP', 'AP'), ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'), ('GO', 'GO'), ('MA', 'MA'), ('MG', 'MG'), ('MS', 'MS'), ('MT', 'MT'), ('PA', 'PA'), ('PB', 'PB'), ('PE', 'PE'), ('PI', 'PI'), ('PR', 'PR'), ('RJ', 'RJ'), ('RO', 'RO'), ('RN', 'RN'), ('RR', 'RR'), ('RS', 'RS'), ('SC', 'SC'), ('SE', 'SE'), ('TO', 'TO')], max_length=2, null=True, verbose_name='UF')),
                ('cidade', models.CharField(blank=True, max_length=120, null=True)),
                ('telefone', models.CharField(blank=True, help_text='Essa informação não estará visível para outros usuários.', max_length=20, null=True, verbose_name='Telefone para Contato')),
                ('bio', models.TextField(blank=True, help_text='Quem é você e com quem gostaria de morar?', null=True, verbose_name='Biografia')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]