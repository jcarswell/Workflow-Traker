# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-10 03:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow_tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='order',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='completedBy',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]