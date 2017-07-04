# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ec', '0010_auto_20170628_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='sol',
            name='sku_id',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=0),
        ),
    ]
