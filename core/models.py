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



def criar_dados():
    #criar cargos
    cargo1 = Cargo.objects.create(nome = "Coordenador(a) pedagógica")
    
    cargo2 = Cargo.objects.create(nome = "Educador(a)")
    
    cargo3 = Cargo.objects.create(nome = "Coordenador(a) social")

    cargo4 = Cargo.objects.create(nome = "Assistente social")

    #Criar usuarios e os funcionarios
    user1 = User.objects.create_user('ednaele', 'ednaele@apae.com', '123456Mm')
    user1.first_name = "Ednaele"
    user1.last_name = "de alguma coisa"
    user1.save()
    funcionario1 = Funcionario.objects.create(user=user1, cargo=cargo1)

    user2 = User.objects.create_user('cintia', 'cintia@apae.com', '123456Mm')
    user2.first_name = "Cintia"
    user2.last_name = "de alguma coisa"
    user2.save()
    funcionario2 = Funcionario.objects.create(user=user2, cargo=cargo2)
    
    user3 = User.objects.create_user('marilia', 'marilia@apae.com', '123456Mm')
    user3.first_name = "Marília"
    user3.last_name = "de alguma coisa"
    user3.save()
    funcionario3 = Funcionario.objects.create(user=user3, cargo=cargo3)

    user4 = User.objects.create_user('juliana', 'juliana@apae.com', '123456Mm')
    user4.first_name = "Juliana"
    user4.last_name = "de alguma coisa"
    user4.save()
    funcionario4 = Funcionario.objects.create(user=user4, cargo=cargo4)

    #Criar as CID
    cid = CID.objects.create(codigo="F00",descricao="Demência na Doença de Alzheimer")
    cid = CID.objects.create(codigo="F01",descricao="Demência Vascular")
    cid = CID.objects.create(codigo="F02",descricao="Demência em Outras Doenças Classificadas em Outra Parte")
    cid = CID.objects.create(codigo="F03",descricao="Demência Não Especificada")
    cid = CID.objects.create(codigo="F04",descricao="Síndrome Amnésica Orgânica Não Induzida Pelo Álcool ou Por Outras Substâncias Psicoativas")
    cid = CID.objects.create(codigo="F05",descricao="Delirium Não Induzido Pelo Álcool ou Por Outras Substâncias Psicoativas")
    cid = CID.objects.create(codigo="F06",descricao="Outros Transtornos Mentais Devidos a Lesão e Disfunção Cerebral e a Doença Física")
    cid = CID.objects.create(codigo="F07",descricao="Transtornos de Personalidade e do Comportamento Devidos a Doença, a Lesão e a Disfunção Cerebral")
    cid = CID.objects.create(codigo="F08",descricao="Transtorno Mental Orgânico ou Sintomático Não Especificado")
    cid = CID.objects.create(codigo="F09",descricao="Transtornos Mentais e Comportamentais Devidos ao Uso de Álcool")
    cid = CID.objects.create(codigo="F10",descricao="Transtornos Mentais e Comportamentais Devidos ao Uso de Opiáceos")
    cid = CID.objects.create(codigo="F11",descricao="Transtornos Mentais e Comportamentais Devidos ao Uso de Canabinóides")


# triger para criar funcionário
# def criar_funcionario(sender, **kwargs):
#     if kwargs['created']:
#         funcionario = Funcionario.objects.create(user=kwargs['instance'])


# post_save.connect(criar_funcionario, sender=User)