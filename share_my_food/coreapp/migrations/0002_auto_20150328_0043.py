# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='deadline',
        ),
        migrations.AddField(
            model_name='food',
            name='expires_in',
            field=models.IntegerField(default=1, help_text=b'(Time in hours)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='food',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
