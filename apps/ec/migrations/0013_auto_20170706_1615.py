# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ec', '0012_sku_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='sku',
            name='description',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='sol',
            name='description',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
