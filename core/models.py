from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


# Create your models here.

class Cargo(models.Model):
    nome = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.nome

class CID(models.Model):
    codigo = models.CharField(max_length=10, blank=True)
    descricao = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return "Código: " + self.codigo + "   Descrição: " + self.descricao


class Usuario(models.Model):
    imagem = models.ImageField(u'Imagem', blank=True, upload_to='usuarios/')
    nome = models.CharField(max_length=200, blank=True)
    cid = models.ForeignKey(CID, on_delete=models.PROTECT, blank=True)
    data_nacimento = models.DateField(u'Data de Nascimento', blank=True)

    @property
    def imagem_url(self):
        if self.imagem:
            return self.imagem.url
        else:
            return None
    
    def __str__(self):
        return "Nome: " + self.nome + "\n CID: " + self.cid.codigo


class Funcionario(models.Model):
    # class Meta:
    #     verbose_name = 'Funcionario'
    #     verbose_name_plural = 'Funcionarios'
    #     ordering = ('nome',)

    # user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='user_profile', null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255, help_text='nome e sobrenome', blank=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return "Nome: " + self.nome



# triger para criar funcionário
def criar_funcionario(sender, **kwargs):
    if kwargs['created']:
        funcionario = Funcionario.objects.create(user=kwargs['instance'])


post_save.connect(criar_funcionario, sender=User)