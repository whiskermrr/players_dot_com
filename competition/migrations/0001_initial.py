# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-05 09:43
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kolejka',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='LeagueType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default='2018-01-05', null=True)),
                ('hostGoals', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('guestGoals', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='MatchFacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incident', models.CharField(choices=[('none', 'brak'), ('goal', 'gol'), ('sub in', 'zmiania wchodzi'), ('sub out', 'zmiana zchodzi'), ('yelow card', 'zolta kartka'), ('red card', 'czerwona kartka')], default='none', max_length=15)),
                ('minute', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(120)])),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competition.Match')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('sname', models.CharField(max_length=100)),
                ('age', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season', models.CharField(max_length=20)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competition.LeagueType')),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competition.LeagueType')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('avatar', models.ImageField(upload_to='media/avatars')),
                ('league', models.ManyToManyField(to='competition.LeagueType')),
            ],
        ),
        migrations.CreateModel(
            name='TeamStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goalsScored', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('goalsLost', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('matchesWon', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('matchesLost', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('matchesDraw', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('scores', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competition.Season')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competition.Team')),
            ],
        ),
        migrations.AddField(
            model_name='table',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competition.Team'),
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competition.Team'),
        ),
        migrations.AddField(
            model_name='matchfacts',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competition.Player'),
        ),
        migrations.AddField(
            model_name='match',
            name='guest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MatchGuest', to='competition.Team'),
        ),
        migrations.AddField(
            model_name='match',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches_as_host', to='competition.Team'),
        ),
        migrations.AddField(
            model_name='match',
            name='kolejka',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='competition.Kolejka'),
        ),
        migrations.AddField(
            model_name='match',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competition.Season'),
        ),
        migrations.AddField(
            model_name='kolejka',
            name='league',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='competition.LeagueType'),
        ),
    ]
