# Generated by Django 2.1 on 2018-10-04 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedagogico', '0010_triagempedagogica'),
    ]

    operations = [
        migrations.AddField(
            model_name='triagempedagogica',
            name='nomeEscola',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]