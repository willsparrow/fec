# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ec', '0002_sol_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='so',
            name='amount',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2),
        ),
        migrations.AddField(
            model_name='so',
            name='total',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=0),
        ),
        migrations.AlterField(
            model_name='so',
            name='cust_id',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=0),
        ),
    ]
