# Generated by Django 3.2.16 on 2025-01-28 07:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_historicalorder'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HistoricalOrder',
        ),
    ]
