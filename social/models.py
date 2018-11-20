from django.contrib.auth.models import User
from django.db import models

from core.models import *

class Triagem(models.Model):
    usuario =  models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True)
    sus = models.CharField(max_length=20, blank=True)

    #dados se é acompanhado com especialista
    acompanhamento_com_especialista = models.BooleanField(blank=True)
    especialista = models.CharField(max_length=200, blank=True)

    #Dados do pai
    nome_pai = models.CharField(max_length=200, blank=True)
    idade_pai = models.IntegerField(default=0, blank=True)
    profissao_pai = models.CharField(max_length=200, blank=True)

    #Dados da mae
    nome_mae = models.CharField(max_length=200, blank=True)
    idade_mae = models.IntegerField(default=0, blank=True)
    profissao_mae = models.CharField(max_length=200, blank=True)

    #dados sobre a renda familiar e seu tipo
    renda_familiar = models.FloatField(default=0, blank=True)
    bpc = models.BooleanField(blank=True)
    bolsa_familia = models.BooleanField(blank=True)
    aposentadoria = models.BooleanField(blank=True)
    benediciario = models.CharField(max_length=200, blank=True)

    #Dados sobre o endereço
    cep = models.CharField(max_length=10, blank=True)
    rua = models.CharField(max_length=300, blank=True)
    numero_da_rua = models.CharField(max_length=10, blank=True)
    bairro = models.CharField(max_length=200, blank=True)
    ponto_de_referencia = models.CharField(max_length=300, blank=True)
    cidade = models.CharField(max_length=200, blank=True)

    #dados de contato
    telefone = models.CharField(max_length=20, blank=True)
    celular = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    #dados para saber se estuda no ensino regular
    estuda_ensino_regular = models.BooleanField(blank=True)
    ano_estuda = models.CharField(max_length=50, blank=True)
    qual = models.CharField(max_length=200, default="", blank=True)
    turma_estuda = models.CharField(max_length=50, blank=True)
    turno_estuda = models.CharField(max_length=50, blank=True)

    #dados saude
    medicacao = models.CharField(max_length=50, blank=True)
    e_i_fisio = models.BooleanField(blank=True)
    e_i_hidro = models.BooleanField(blank=True)
    e_i_fono = models.BooleanField(blank=True)
    e_i_to = models.BooleanField(blank=True)
    e_i_psi = models.BooleanField(blank=True)
    e_i_ondonto = models.BooleanField(blank=True)
    e_i_medico = models.BooleanField(blank=True)
    e_i_psicopedagoga = models.BooleanField(blank=True)
    e_i_pedagogia = models.BooleanField(blank=True)
    
    observacoes = models.CharField(max_length=50, blank=True)
    assinatura_proficinal = models.ForeignKey(Funcionario, on_delete=models.PROTECT, blank=True)

    data_da_triagem = models.DateField('Data da Triagem', blank=True)

    def __str__(self):
        return "Nome: "+self.usuario.nome+"\n Pai: "+self.nome_pai+"\n Mãe: "+self.nome_mae

class Visita(models.Model):
    usuario =  models.ForeignKey(Usuario, on_delete=models.PROTECT, blank=True)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.PROTECT, blank=True)
    data_visita = models.DateField('Data Visita', blank=True)
    observacoes = models.CharField(max_length=300, blank=True)
    realizada = models.BooleanField(default=False, blank=True)
    local = models.CharField(max_length=300, blank=True, default='')
    
    def __str__(self):
        return "Nome do usuário: "+self.usuario.nome+"\n Data da visita: "+str(self.data_visita.day)+"/"+str(self.data_visita.month)+"/"+str(self.data_visita.year)+"\n Nome do proficinal: "+self.funcionario.user.first_name

class Lista(models.Model):
    posicao = models.IntegerField(default=0, blank=True)
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True)

class Evento(models.Model):
    nome = models.CharField(max_length=100, blank=True)
    data_inicio = models.DateField('Data de início', blank=True)
    data_fim = models.DateField('Data do término', blank=True)
    lista = models.ManyToManyField(Lista, blank=True)
    def __str__(self):
        return "Evento: "+self.nome

