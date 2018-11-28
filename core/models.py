from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from datetime import datetime

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
    class Meta:
        ordering = ['nome']
    imagem = models.ImageField(u'Imagem', blank=True, upload_to='usuarios/')
    nome = models.CharField(max_length=200, blank=True)
    cid = models.ForeignKey(CID, on_delete=models.PROTECT, blank=True)
    data_nacimento = models.DateField(u'Data de Nascimento', blank=True)
    situacao = models.CharField(max_length=15, blank=True,default="Ativo")

    @property
    def imagem_url(self):
        if self.imagem:
            return self.imagem.url
        else:
            return None
    
    def __str__(self):
        return "Nome: " + self.nome + "\n CID: " + self.cid.codigo

class Funcionario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT, blank=True, null=True)
    imagem = models.ImageField(u'Imagem', blank=True, upload_to='funcionarios/')

    @property
    def imagem_url(self):
        if self.imagem:
            return self.imagem.url
        else:
            return None
    
    def __str__(self):
        return "Nome: " + self.user.first_name +" "+self.user.last_name

class Registro_acesso(models.Model):
    usuario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    data_acesso = models.DateTimeField(default=datetime.now)
    def __str__(self):
        data = str(self.data_acesso.day)+"/"+str(self.data_acesso.month)+"/"+str(self.data_acesso.year)+" "+str(self.data_acesso.hour)+":"+str(self.data_acesso.minute)+":"+str(self.data_acesso.second)
        return "Nome: " + self.usuario.user.first_name +" "+self.usuario.user.last_name+ "   | Data: "+ data

class Registro_acao(models.Model):
    data_acao = models.DateTimeField(default=datetime.now)
    usuario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)    
    dado = models.CharField(max_length=50)
    id_dado = models.IntegerField(default=0)





# triger para criar funcionário
# def criar_funcionario(sender, **kwargs):
#     if kwargs['created']:
#         funcionario = Funcionario.objects.create(user=kwargs['instance'])


# post_save.connect(criar_funcionario, sender=User)