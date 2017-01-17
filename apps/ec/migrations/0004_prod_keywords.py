# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ec', '0003_auto_20170111_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='prod',
            name='keywords',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
