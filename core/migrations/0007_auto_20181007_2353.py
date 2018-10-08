# Generated by Django 2.1 on 2018-10-07 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20181005_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='data_nacimento',
            field=models.DateField(verbose_name='Data de Nascimento'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='imagem',
            field=models.ImageField(blank=True, upload_to='media/usuarios/', verbose_name='Logo'),
        ),
    ]
