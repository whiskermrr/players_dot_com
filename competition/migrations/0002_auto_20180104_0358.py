# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-04 02:58
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='table',
            old_name='name1',
            new_name='league',
        ),
        migrations.RenameField(
            model_name='table',
            old_name='name',
            new_name='team',
        ),
        migrations.AlterField(
            model_name='match',
            name='guestGoals',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='match',
            name='hostGoals',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
