# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cust',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
                ('role', models.CharField(max_length=100, null=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('birthday', models.DateTimeField(null=True)),
                ('sex', models.CharField(max_length=100, null=True)),
                ('photo', models.CharField(max_length=200, null=True)),
                ('shop', models.CharField(max_length=100, null=True)),
                ('company', models.CharField(max_length=100, null=True)),
                ('mobilephone', models.CharField(max_length=100, null=True)),
                ('telephone', models.CharField(max_length=100, null=True)),
                ('email', models.CharField(max_length=100, null=True)),
                ('province', models.CharField(max_length=100, null=True)),
                ('city', models.CharField(max_length=100, null=True)),
                ('country', models.CharField(max_length=100, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('created_date', models.DateTimeField(null=True)),
                ('updated_date', models.DateTimeField(null=True)),
                ('status', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
            ],
            options={
                'db_table': 't_cust',
            },
        ),
        migrations.CreateModel(
            name='Prod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('title', models.CharField(max_length=100, null=True)),
                ('code', models.CharField(max_length=100, null=True)),
                ('price', models.DecimalField(null=True, max_digits=10, decimal_places=2)),
                ('qty', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
                ('unit', models.CharField(max_length=100, null=True)),
                ('spec', models.CharField(max_length=100, null=True)),
                ('created_date', models.DateTimeField(null=True)),
                ('updated_date', models.DateTimeField(null=True)),
                ('brand', models.CharField(max_length=100, null=True)),
                ('company', models.CharField(max_length=100, null=True)),
                ('category', models.CharField(max_length=100, null=True)),
                ('status', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
                ('img_l', models.CharField(max_length=200, null=True)),
                ('img_m', models.CharField(max_length=200, null=True)),
                ('img_s', models.CharField(max_length=200, null=True)),
                ('img_t', models.CharField(max_length=200, null=True)),
                ('description', models.CharField(max_length=1000, null=True)),
                ('size', models.CharField(max_length=100, null=True)),
                ('sex', models.CharField(max_length=100, null=True)),
                ('color', models.CharField(max_length=100, null=True)),
                ('weight', models.CharField(max_length=100, null=True)),
                ('age', models.CharField(max_length=100, null=True)),
            ],
            options={
                'db_table': 't_prod',
            },
        ),
        migrations.CreateModel(
            name='So',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cust_id', models.DecimalField(null=True, max_digits=10, decimal_places=2)),
                ('cust_name', models.CharField(max_length=100, null=True)),
                ('cust_mobilephone', models.CharField(max_length=100, null=True)),
                ('cust_telephone', models.CharField(max_length=100, null=True)),
                ('cust_email', models.CharField(max_length=100, null=True)),
                ('shop', models.CharField(max_length=100, null=True)),
                ('company', models.CharField(max_length=100, null=True)),
                ('province', models.CharField(max_length=100, null=True)),
                ('city', models.CharField(max_length=100, null=True)),
                ('country', models.CharField(max_length=100, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('created_date', models.DateTimeField(null=True)),
                ('updated_date', models.DateTimeField(null=True)),
                ('status', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
            ],
            options={
                'db_table': 't_so',
            },
        ),
        migrations.CreateModel(
            name='Sol',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('so_id', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
                ('cust_id', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
                ('prod_id', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
                ('img_t', models.CharField(max_length=100, null=True)),
                ('price', models.DecimalField(null=True, max_digits=10, decimal_places=2)),
                ('qty', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
                ('created_date', models.DateTimeField(null=True)),
                ('updated_date', models.DateTimeField(null=True)),
                ('status', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
            ],
            options={
                'db_table': 't_sol',
            },
        ),
    ]
