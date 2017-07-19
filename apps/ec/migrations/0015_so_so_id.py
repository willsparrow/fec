# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ec', '0014_wxpaylog_wxpayqrcode_wxpayresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='so',
            name='so_id',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=0),
        ),
    ]
