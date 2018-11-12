# Generated by Django 2.1.2 on 2018-11-12 09:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0013_auto_20181110_1240'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descrizione', models.TextField(blank=True)),
                ('data_upload', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(upload_to='documenti/%Y/%m/')),
            ],
            options={
                'verbose_name_plural': 'Documenti',
            },
        ),
        migrations.AlterModelOptions(
            name='prestito',
            options={'get_latest_by': '-data_richiesta', 'verbose_name_plural': 'Prestiti'},
        ),
        migrations.AlterField(
            model_name='prestito',
            name='stato',
            field=models.CharField(choices=[('RC', 'Richiesto'), ('IC', 'In corso'), ('CN', 'Concluso')], max_length=2),
        ),
        migrations.CreateModel(
            name='DocumentoAmministratore',
            fields=[
                ('documento_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.Documento')),
            ],
            options={
                'verbose_name_plural': 'Documenti Amministratore',
            },
            bases=('core.documento',),
        ),
        migrations.AddField(
            model_name='documento',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
