# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ec', '0019_auto_20170801_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='smslog',
            name='message_content',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
