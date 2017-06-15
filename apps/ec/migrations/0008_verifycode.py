# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ec', '0007_auto_20170615_1029'),
    ]

    operations = [
        migrations.CreateModel(
            name='Verifycode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mobilephone', models.CharField(max_length=100, null=True)),
                ('verifycode', models.CharField(max_length=100, null=True)),
                ('status', models.CharField(max_length=100, null=True)),
                ('created_date', models.DateTimeField(null=True)),
                ('updated_date', models.DateTimeField(null=True)),
                ('expire_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 't_verifycode',
            },
        ),
    ]
