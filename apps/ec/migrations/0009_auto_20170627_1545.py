# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ec', '0008_verifycode'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProdProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prod_id', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
                ('name', models.CharField(max_length=100, null=True)),
                ('status', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
                ('created_date', models.DateTimeField(null=True)),
                ('updated_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 't_prod_property',
            },
        ),
        migrations.CreateModel(
            name='ProdPv',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prod_id', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
                ('property_id', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
                ('property_name', models.CharField(max_length=100, null=True)),
                ('value', models.CharField(max_length=100, null=True)),
                ('img_url', models.CharField(max_length=100, null=True)),
                ('status', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
                ('created_date', models.DateTimeField(null=True)),
                ('updated_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 't_prod_pv',
            },
        ),
        migrations.CreateModel(
            name='Sku',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prod_id', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
                ('code', models.CharField(max_length=100, null=True)),
                ('price', models.DecimalField(null=True, max_digits=10, decimal_places=2)),
                ('qty', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
                ('img_url', models.CharField(max_length=100, null=True)),
                ('pv', models.CharField(max_length=1000, null=True)),
                ('status', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
                ('created_date', models.DateTimeField(null=True)),
                ('updated_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 't_sku',
            },
        ),
        migrations.RenameField(
            model_name='sol',
            old_name='img_t',
            new_name='img_url',
        ),
        migrations.RemoveField(
            model_name='prod',
            name='age',
        ),
        migrations.RemoveField(
            model_name='prod',
            name='color',
        ),
        migrations.RemoveField(
            model_name='prod',
            name='img_l',
        ),
        migrations.RemoveField(
            model_name='prod',
            name='img_m',
        ),
        migrations.RemoveField(
            model_name='prod',
            name='img_s',
        ),
        migrations.RemoveField(
            model_name='prod',
            name='img_t',
        ),
        migrations.RemoveField(
            model_name='prod',
            name='sex',
        ),
        migrations.RemoveField(
            model_name='prod',
            name='size',
        ),
        migrations.RemoveField(
            model_name='prod',
            name='weight',
        ),
        migrations.RemoveField(
            model_name='proddetail',
            name='img',
        ),
        migrations.RemoveField(
            model_name='prodthumb',
            name='img',
        ),
        migrations.AddField(
            model_name='prod',
            name='img_url',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='proddetail',
            name='img_url',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='prodthumb',
            name='img_url',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
