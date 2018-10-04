# Generated by Django 2.1.1 on 2018-09-24 22:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pedagogico', '0002_usuarioturma'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfessorTurma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pedagogico.Funcionario')),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pedagogico.Turma')),
            ],
        ),
    ]