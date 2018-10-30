# Generated by Django 2.1.2 on 2018-10-30 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Autore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('cognome', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('cognome', 'nome'),
            },
        ),
        migrations.CreateModel(
            name='Editore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Genere',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('nome',),
            },
        ),
        migrations.CreateModel(
            name='Libro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disponibile', models.BooleanField()),
                ('data_restituzione', models.DateField(blank=True, null=True)),
                ('isbn', models.CharField(max_length=13, unique=True, verbose_name='ISBN')),
                ('titolo', models.CharField(max_length=100)),
                ('descrizione', models.TextField(blank=True)),
                ('collana', models.CharField(max_length=100)),
                ('autori', models.ManyToManyField(to='core.Autore')),
                ('editore', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Editore')),
                ('genere', models.ManyToManyField(to='core.Genere')),
            ],
            options={
                'ordering': ('titolo',),
            },
        ),
    ]
