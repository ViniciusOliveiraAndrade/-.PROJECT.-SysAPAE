# Generated by Django 2.1 on 2018-09-26 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0007_auto_20180925_1855'),
    ]

    operations = [
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('cargo', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('cid', models.CharField(max_length=20)),
                ('data_nacimento', models.DateTimeField(verbose_name='Data de Nascimento')),
            ],
        ),
        migrations.RemoveField(
            model_name='triagem',
            name='imagem',
        ),
        migrations.AlterField(
            model_name='triagem',
            name='acompanhamento_com_especialista',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='triagem',
            name='assinatura_proficinal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='social.Funcionario'),
        ),
        migrations.AlterField(
            model_name='triagem',
            name='especialista',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='triagem',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='social.Usuario'),
        ),
        migrations.AlterField(
            model_name='visita',
            name='funcionario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='social.Funcionario'),
        ),
        migrations.AlterField(
            model_name='visita',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='social.Usuario'),
        ),
    ]