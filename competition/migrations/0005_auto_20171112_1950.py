# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-12 18:50
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0004_auto_20171112_0320'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='league',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='competition.LeagueType'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='table',
            name='points',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
