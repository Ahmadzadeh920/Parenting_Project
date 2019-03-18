# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-07 08:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Farzand_Parvari_app', '0028_auto_20190307_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='punishment_behavior',
            name='Date_Time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='situation_defficult_behavior',
            name='Date_Time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='punishment_behavior',
            name='result',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
