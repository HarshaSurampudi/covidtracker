# Generated by Django 3.0.5 on 2020-04-12 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0006_auto_20200411_1918'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DailyStat',
        ),
        migrations.DeleteModel(
            name='Entry',
        ),
    ]