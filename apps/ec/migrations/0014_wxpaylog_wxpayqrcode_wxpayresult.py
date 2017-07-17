# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ec', '0013_auto_20170706_1615'),
    ]

    operations = [
        migrations.CreateModel(
            name='WXPayLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('so_id', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
                ('appid', models.CharField(max_length=100, null=True)),
                ('mch_id', models.CharField(max_length=100, null=True)),
                ('device_info', models.CharField(max_length=100, null=True)),
                ('nonce_str', models.CharField(max_length=100, null=True)),
                ('sign', models.CharField(max_length=100, null=True)),
                ('sign_type', models.CharField(max_length=100, null=True)),
                ('body', models.CharField(max_length=100, null=True)),
                ('detail', models.CharField(max_length=10000, null=True)),
                ('attach', models.CharField(max_length=200, null=True)),
                ('out_trade_no', models.CharField(max_length=100, null=True)),
                ('fee_type', models.CharField(max_length=100, null=True)),
                ('total_fee', models.CharField(max_length=100, null=True)),
                ('spbill_create_ip', models.CharField(max_length=100, null=True)),
                ('notify_url', models.CharField(max_length=100, null=True)),
                ('trade_type', models.CharField(max_length=100, null=True)),
                ('openid', models.CharField(max_length=100, null=True)),
                ('created_date', models.DateTimeField(null=True)),
                ('updated_date', models.DateTimeField(null=True)),
                ('status', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
            ],
            options={
                'db_table': 't_wxpay_log',
            },
        ),
        migrations.CreateModel(
            name='WXPayQrcode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('so_id', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
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
                ('code_url', models.CharField(max_length=100, null=True)),
                ('qrcode_url', models.CharField(max_length=100, null=True)),
                ('created_date', models.DateTimeField(null=True)),
                ('updated_date', models.DateTimeField(null=True)),
                ('status', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
            ],
            options={
                'db_table': 't_wxpay_qrcode',
            },
        ),
        migrations.CreateModel(
            name='WXPayResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('so_id', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
                ('return_code', models.CharField(max_length=100, null=True)),
                ('return_msg', models.CharField(max_length=100, null=True)),
                ('appid', models.CharField(max_length=100, null=True)),
                ('mch_id', models.CharField(max_length=100, null=True)),
                ('device_info', models.CharField(max_length=100, null=True)),
                ('nonce_str', models.CharField(max_length=100, null=True)),
                ('sign', models.CharField(max_length=100, null=True)),
                ('sign_type', models.CharField(max_length=100, null=True)),
                ('result_code', models.CharField(max_length=100, null=True)),
                ('err_code', models.CharField(max_length=100, null=True)),
                ('err_code_des', models.CharField(max_length=100, null=True)),
                ('openid', models.CharField(max_length=200, null=True)),
                ('is_subscribe', models.CharField(max_length=100, null=True)),
                ('trade_type', models.CharField(max_length=100, null=True)),
                ('bank_type', models.CharField(max_length=100, null=True)),
                ('total_fee', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
                ('fee_type', models.CharField(max_length=100, null=True)),
                ('cash_fee', models.CharField(max_length=100, null=True)),
                ('cash_fee_type', models.CharField(max_length=100, null=True)),
                ('coupon_fee', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
                ('coupon_count', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
                ('transaction_id', models.CharField(max_length=100, null=True)),
                ('out_trade_no', models.CharField(max_length=100, null=True)),
                ('attach', models.CharField(max_length=200, null=True)),
                ('time_end', models.CharField(max_length=100, null=True)),
                ('created_date', models.DateTimeField(null=True)),
                ('updated_date', models.DateTimeField(null=True)),
                ('status', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
            ],
            options={
                'db_table': 't_wxpay_result',
            },
        ),
    ]
