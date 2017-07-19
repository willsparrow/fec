# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ec', '0016_auto_20170719_1351'),
    ]

    operations = [
        migrations.RenameField(
            model_name='so',
            old_name='so_no',
            new_name='no',
        ),
    ]
