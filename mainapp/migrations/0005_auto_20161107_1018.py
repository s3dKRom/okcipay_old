# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-07 08:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20161022_1628'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_bank', models.DecimalField(decimal_places=0, max_digits=6)),
                ('bank_name', models.TextField()),
            ],
            options={
                'db_table': 'banks',
            },
        ),
        migrations.CreateModel(
            name='Currencies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_currency', models.DecimalField(decimal_places=0, max_digits=3)),
                ('currency_int', models.TextField()),
                ('currency_loc', models.TextField()),
            ],
            options={
                'db_table': 'currencies',
            },
        ),
        migrations.AlterField(
            model_name='balances',
            name='dt',
            field=models.TextField(),
        ),
    ]
