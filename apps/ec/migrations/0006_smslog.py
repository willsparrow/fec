# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ec', '0005_proddetail_prodthumb'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmsLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_id', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
                ('receiver', models.CharField(max_length=100, null=True)),
                ('message_id', models.CharField(max_length=100, null=True)),
                ('created_date', models.DateTimeField(null=True)),
                ('updated_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 't_sms_log',
            },
        ),
    ]
