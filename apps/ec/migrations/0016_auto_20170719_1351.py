# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ec', '0015_so_so_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='so',
            old_name='so_id',
            new_name='so_no',
        ),
        migrations.AddField(
            model_name='sol',
            name='so_no',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=0),
        ),
        migrations.AddField(
            model_name='wxpaylog',
            name='so_no',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=0),
        ),
        migrations.AddField(
            model_name='wxpayqrcode',
            name='so_no',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=0),
        ),
        migrations.AddField(
            model_name='wxpayresult',
            name='so_no',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=0),
        ),
    ]
