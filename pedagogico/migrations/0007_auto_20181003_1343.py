# Generated by Django 2.1 on 2018-10-03 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedagogico', '0006_auto_20181003_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aula',
            name='data',
            field=models.DateTimeField(verbose_name='Data da Aula'),
        ),
    ]