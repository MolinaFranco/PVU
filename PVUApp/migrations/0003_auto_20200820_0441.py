# Generated by Django 2.2.13 on 2020-08-20 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PVUApp', '0002_auto_20200819_2149'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Observacionpsico',
            new_name='Observacion_psico',
        ),
        migrations.RemoveField(
            model_name='asistencia',
            name='Chico',
        ),
        migrations.AddField(
            model_name='asistencia',
            name='Chico',
            field=models.ManyToManyField(to='PVUApp.Chico'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='nivel',
            field=models.CharField(choices=[('1', 'Admin'), ('2', 'Psicopedagogo'), ('3', 'Psicologo'), ('4', 'Cocinero')], max_length=1, null=True),
        ),
    ]