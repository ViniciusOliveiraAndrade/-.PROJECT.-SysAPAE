# Generated by Django 2.1 on 2018-09-17 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='triagem',
            name='qual',
            field=models.CharField(default='Qualquer', max_length=200),
        ),
    ]
