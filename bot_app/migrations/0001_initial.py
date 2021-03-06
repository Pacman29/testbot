# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-28 07:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('C', 'Current'), ('M', 'Modular')], max_length=2)),
                ('task', models.TextField(max_length=1000)),
                ('last_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('subject_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot_app.Subjects')),
            ],
        ),
    ]
