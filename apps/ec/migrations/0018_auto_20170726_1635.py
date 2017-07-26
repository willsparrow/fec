# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ec', '0017_auto_20170719_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='WXPayMweb',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('so_id', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
                ('so_no', models.DecimalField(null=True, max_digits=20, decimal_places=0)),
                ('appid', models.CharField(max_length=100, null=True)),
                ('mch_id', models.CharField(max_length=100, null=True)),
                ('device_info', models.CharField(max_length=100, null=True)),
                ('nonce_str', models.CharField(max_length=100, null=True)),
                ('sign', models.CharField(max_length=100, null=True)),
                ('sign_type', models.CharField(max_length=100, null=True)),
                ('result_code', models.CharField(max_length=100, null=True)),
                ('err_code', models.CharField(max_length=100, null=True)),
                ('err_code_des', models.CharField(max_length=100, null=True)),
                ('trade_type', models.CharField(max_length=100, null=True)),
                ('prepay_id', models.CharField(max_length=100, null=True)),
                ('mweb_url', models.CharField(max_length=100, null=True)),
                ('created_date', models.DateTimeField(null=True)),
                ('updated_date', models.DateTimeField(null=True)),
                ('status', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
            ],
            options={
                'db_table': 't_wxpay_mweb',
            },
        ),
        migrations.RemoveField(
            model_name='wxpayqrcode',
            name='qrcode_url',
        ),
    ]
