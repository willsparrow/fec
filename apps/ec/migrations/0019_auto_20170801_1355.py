# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ec', '0018_auto_20170726_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wxpaymweb',
            name='mweb_url',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
