# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-20 10:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20170119_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='imageUrl',
            field=models.ImageField(default='images/default.jpg', max_length=256, upload_to='static/images/im', verbose_name='Картинка'),
        ),
        migrations.AlterField(
            model_name='eventprevious',
            name='imageUrl',
            field=models.ImageField(default='images/default.jpg', max_length=256, upload_to='static/images/im', verbose_name='Картинка'),
        ),
    ]
