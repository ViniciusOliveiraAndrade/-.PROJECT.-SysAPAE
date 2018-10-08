from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Usuario(models.Model):
    imagem = models.ImageField(u'Imagem', blank=True, upload_to='usuarios/')
    nome = models.CharField(max_length=200)
    cid = models.CharField(max_length=20)
    data_nacimento = models.DateField(u'Data de Nascimento',blank=True)

    @property
    def imagem_url(self):
        if self.imagem:
            return self.imagem.url
        else:
            return None
    
    def __str__(self):
        return "Nome: " + self.nome + "\n CID: " + self.cid


class Cargo(models.Model):
    descricao = models.CharField(max_length=255, help_text='nome e sobrenome')

    def __str__(self):
        return self.descricao


class Funcionario(models.Model):
    # class Meta:
    #     verbose_name = 'Funcionario'
    #     verbose_name_plural = 'Funcionarios'
    #     ordering = ('nome',)

    # user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='user_profile', null=True)
    nome = models.CharField(max_length=255, help_text='nome e sobrenome')
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT)

    def __str__(self):
        return self.nome
