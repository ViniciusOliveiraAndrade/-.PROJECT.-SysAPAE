from django.db import models
from core.models import *
from social.models import Triagem
# Create your models here.

class Turma(models.Model):
    nome = models.CharField(max_length=50)
    turno = models.BooleanField()
    ususario = models.ManyToManyField(Usuario, blank=True)
    # aulas = models.ManyToManyField()
    professor = models.ManyToManyField(Funcionario)

    def __str__(self):
        return "Turma: "+self.nome


class Frequencia(models.Model):
    presente = models.BooleanField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)


    def __str__(self):
        return "Aula: "+self.conteudo

class Aula(models.Model):
    data = models.DateField('Data da Aula')
    conteudo = models.CharField(max_length=500)
    titulo = models.CharField(max_length=50)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, blank=False)
    frequencia = models.ManyToManyField(Frequencia)
    avaliacaoAula = models.CharField(max_length=500, blank=True)
    situacao = models.BooleanField(default='True')

    def __str__(self):
        return "Aula: "+self.titulo


class TriagemPedagogica(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, blank=False)
    data = models.DateField()
    estuda = models.BooleanField()
    anoEscolar = models.IntegerField()
    nomeEscola = models.CharField(max_length=50, blank=True)
    municipio = models.CharField(max_length=50)
    horarioApae = models.BooleanField()
    # Aqui fica um atributo para os dias da semana

    alimentacao = models.TextField()
    medicacao = models.TextField()
    composicaoFamiliar = models.TextField()
    controleUrinario = models.BooleanField()
    controleEsfincter = models.BooleanField()
    controleObservacao = models.TextField()

    cuidador = models.CharField(max_length=50)
    responsavel = models.CharField(max_length=50)
    horarioDormir = models.FloatField()
    horarioAcordar = models.FloatField()
    dormeCom = models.CharField(max_length=50)

#     Aspecto de Desenvolvimento

    falaBem = models.BooleanField()
    comunicacaoGestos = models.BooleanField()
    gagueira = models.BooleanField()
    enxergaBem = models.BooleanField()
    destro = models.BooleanField()
    fazBalbucio = models.BooleanField()

#     Aspecto fisico motor

    anda = models.BooleanField()
    seguraLapis = models.BooleanField()
    sentaCorretamente = models.BooleanField()
    caiMuito = models.BooleanField()
    cansaFacil = models.BooleanField()

#     Aspecto Emocional

    afetuodo = models.BooleanField()
    medroso = models.BooleanField()
    agressivo = models.BooleanField()
    reageContrariado = models.BooleanField()
    tique = models.BooleanField()
    choraFacilidade = models.BooleanField()

#     Aspecto Social

    sabeEspear = models.BooleanField()
    obedeceOrdens = models.BooleanField()
    fazAmizade = models.BooleanField()
    isolase = models.BooleanField()
    compartilha = models.BooleanField()
    seRelaciona = models.BooleanField()

#     Aspecto Intelectual

    # pronucia corretamente as palavras
    expressaPensanetos = models.BooleanField()
    transmiteRecados = models.BooleanField()
    # Atenta para instruções fazendo o que é pedido
    descricaoUsuario = models.TextField()




