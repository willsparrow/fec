# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ec', '0006_smslog'),
    ]

    operations = [
        migrations.CreateModel(
            name='Md5',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original', models.CharField(max_length=100, null=True)),
                ('md5', models.CharField(max_length=100, null=True)),
                ('created_date', models.DateTimeField(null=True)),
                ('updated_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 't_md5',
            },
        ),
        migrations.AddField(
            model_name='smslog',
            name='type',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
