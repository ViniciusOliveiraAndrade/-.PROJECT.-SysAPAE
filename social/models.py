from django.contrib.auth.models import User
from django.db import models

from core.models import *

class Triagem(models.Model):
    usuario =  models.ForeignKey(Usuario, on_delete=models.CASCADE)
    sus = models.CharField(max_length=20)

    #dados se é acompanhado com especialista
    acompanhamento_com_especialista = models.BooleanField()
    especialista = models.CharField(max_length=200)

    #Dados do pai
    nome_pai = models.CharField(max_length=200)
    idade_pai = models.IntegerField(default=0)
    profissao_pai = models.CharField(max_length=200)

    #Dados da mae
    nome_mae = models.CharField(max_length=200)
    idade_mae = models.IntegerField(default=0)
    profissao_mae = models.CharField(max_length=200)

    #dados sobre a renda familiar e seu tipo
    renda_familiar = models.FloatField(default=0)
    bpc = models.BooleanField()
    bolsa_familia = models.BooleanField()
    aposentadoria = models.BooleanField()
    benediciario = models.CharField(max_length=200)

    #Dados sobre o endereço
    rua = models.CharField(max_length=300)
    numero_da_rua = models.CharField(max_length=10)
    bairro = models.CharField(max_length=200)
    ponto_de_referencia = models.CharField(max_length=300)
    cidade = models.CharField(max_length=200)

    #dados de contato
    telefone = models.CharField(max_length=20)
    celular = models.CharField(max_length=20)
    email = models.EmailField()

    #dados para saber se estuda no ensino regular
    estuda_ensino_regular = models.BooleanField()
    ano_estuda = models.CharField(max_length=50)
    qual = models.CharField(max_length=200, default="Qualquer")
    turma_estuda = models.CharField(max_length=50)
    turno_estuda = models.CharField(max_length=50)

    observacoes = models.CharField(max_length=50)
    assinatura_proficinal = models.ForeignKey(Funcionario, on_delete=models.PROTECT)

    data_da_triagem = models.DateTimeField('Data da Triagem')

    def __str__(self):
        return "Nome: "+self.usuario.nome+"\n Pai: "+self.nome_pai+"\n Mãe: "+self.nome_mae

class Visita(models.Model):
    usuario =  models.ForeignKey(Usuario, on_delete=models.PROTECT)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.PROTECT)
    data_visita = models.DateTimeField('Data Visita')
    observacoes = models.CharField(max_length=300)
    realizada = models.BooleanField(default=False)
    def __str__(self):
        return "Nome do usuário: "+self.usuario.nome+"\n Data da visita: "+self.data_visita+"\n Nome do proficinal: "+self.funcionario.nome

class Evento(models.Model):
    nome = models.CharField(max_length=100)
    data_inicio = models.DateTimeField('Data de início')
    data_fim = models.DateTimeField('Data do término')
    lista = models.ManyToManyField(Lista, on_delete=models.CASCADE)

class Lista(models.Model):
    posicao = mmodels.IntegerField(default=0)
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)


# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
#     