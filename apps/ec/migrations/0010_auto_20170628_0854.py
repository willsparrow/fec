# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ec', '0009_auto_20170627_1545'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sku',
            old_name='pv',
            new_name='pvs',
        ),
    ]
