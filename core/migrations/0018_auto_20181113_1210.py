# Generated by Django 2.1.2 on 2018-11-13 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20181113_0955'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prestito',
            old_name='data_prestito',
            new_name='data_inizio',
        ),
        migrations.RenameField(
            model_name='prestito',
            old_name='data_restituzione',
            new_name='data_scadenza',
        ),
    ]
