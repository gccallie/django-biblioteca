# Generated by Django 2.1.2 on 2018-11-06 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20181105_1852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profilo',
            name='utente',
        ),
    ]