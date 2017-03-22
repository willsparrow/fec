# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ec', '0004_prod_keywords'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProdDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prod_id', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
                ('img', models.CharField(max_length=200, null=True)),
                ('seq', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
                ('created_date', models.DateTimeField(null=True)),
                ('updated_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 't_prod_detail',
            },
        ),
        migrations.CreateModel(
            name='ProdThumb',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prod_id', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
                ('img', models.CharField(max_length=200, null=True)),
                ('seq', models.DecimalField(null=True, max_digits=10, decimal_places=0)),
                ('created_date', models.DateTimeField(null=True)),
                ('updated_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 't_prod_thumb',
            },
        ),
    ]
