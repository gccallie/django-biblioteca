# Generated by Django 2.1.2 on 2018-11-09 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20181108_1643'),
    ]

    operations = [
        migrations.CreateModel(
            name='Segnalazione',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('D', 'Danneggiamento'), ('R', 'Ritardo consegna')], max_length=10)),
                ('data', models.DateField(auto_now_add=True)),
                ('descrizione', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Segnalazioni',
            },
        ),
        migrations.AddField(
            model_name='profilo',
            name='segnalazioni',
            field=models.ManyToManyField(blank=True, to='core.Segnalazione'),
        ),
    ]
