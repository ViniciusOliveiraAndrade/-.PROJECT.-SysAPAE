# Generated by Django 2.1 on 2018-09-25 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0004_auto_20180925_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triagem',
            name='especialista',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
