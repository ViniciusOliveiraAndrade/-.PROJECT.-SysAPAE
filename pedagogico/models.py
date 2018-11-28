from django.db import models
from core.models import *
from social.models import Triagem
# Create your models here.
from datetime import datetime


class Frequencia(models.Model):
    falta = models.BooleanField(default=False)
    usuario = models.ManyToManyField(Usuario)
    desempenho = models.CharField(max_length=100)


    def __str__(self):
        return "Frequência: "

class Aula(models.Model):
    data = models.DateField('Data da Aula')
    conteudo = models.CharField(max_length=500)
    titulo = models.CharField(max_length=50)
    frequencia = models.ForeignKey(Frequencia, on_delete=models.CASCADE, blank=True)
    avaliacaoAula = models.CharField(max_length=500, blank=True)
    situacao = models.BooleanField(default='True')

    def __str__(self):
        return "Aula: "+self.titulo

class Turma(models.Model):
    nome = models.CharField(max_length=50)
    turno = models.BooleanField()
    ususario = models.ManyToManyField(Usuario, blank=True)
    professor = models.ForeignKey(Funcionario,on_delete=models.PROTECT)
    aula = models.ManyToManyField(Aula)

    def __str__(self):
        return "Turma: "+self.nome



class TriagemPedagogica(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, blank=False)
    data = models.DateField(default=datetime.now)

    segunda = models.BooleanField(blank=True)
    terca = models.BooleanField(blank=True)
    quarta = models.BooleanField(blank=True)
    quinta = models.BooleanField(blank=True)
    sexta = models.BooleanField(blank=True)

    alimentacao = models.TextField(blank=True)
    composicaoFamiliar = models.TextField(blank=True)
    controleUrinario = models.BooleanField(blank=True)
    controleEsfincter = models.BooleanField(blank=True)
    controleObservacao = models.TextField(blank=True)

    # PEDAGOGICO
    musica = models.CharField(max_length=1, blank=True)
    danca = models.CharField(max_length=1, blank=True)
    pintura = models.CharField(max_length=1, blank=True)
    jiujitsu = models.CharField(max_length=1, blank=True)
    edFisica = models.CharField(max_length=1, blank=True)
    informatica = models.CharField(max_length=1, blank=True)
    robotica = models.CharField(max_length=1, blank=True)
    teatro = models.CharField(max_length=1, blank=True)

    cuidador = models.CharField(max_length=50, blank=True)
    responsavel = models.CharField(max_length=50, blank=True)
    horarioDormir = models.TimeField(blank=True)
    horarioAcordar = models.TimeField(blank=True)
    dormeCom = models.CharField(max_length=50, blank=True)

#     Aspecto de Desenvolvimento

    falaBem = models.CharField(max_length=1, blank=True)
    comunicacaoGestos = models.CharField(max_length=1, blank=True)
    gagueira = models.CharField(max_length=1, blank=True)
    enxergaBem = models.CharField(max_length=1, blank=True)
    destro = models.CharField(max_length=1, blank=True)
    esquerda = models.CharField(max_length=1, blank=True)
    fazBalbucio = models.CharField(max_length=1, blank=True)

#     Aspecto fisico motor

    anda = models.CharField(max_length=1, blank=True)
    seguraLapis = models.CharField(max_length=1, blank=True)
    sentaCorretamente = models.CharField(max_length=1, blank=True)
    caiMuito = models.CharField(max_length=1, blank=True)
    cansaFacil = models.CharField(max_length=1, blank=True)

#     Aspecto Emocional

    solicitaAfeto = models.CharField(max_length=1, blank=True)
    demonstraAfeto = models.CharField(max_length=1, blank=True)
    medroso = models.CharField(max_length=1, blank=True)
    agressivo = models.CharField(max_length=1, blank=True)
    reageContrariado = models.CharField(max_length=1, blank=True)
    tique = models.CharField(max_length=1, blank=True)
    choraFacilidade = models.CharField(max_length=1, blank=True)

#     Aspecto Social

    sabeEspear = models.CharField(max_length=1, blank=True)
    obedeceOrdens = models.CharField(max_length=1, blank=True)
    fazAmizade = models.CharField(max_length=1, blank=True)
    isolase = models.CharField(max_length=1, blank=True)
    compartilha = models.CharField(max_length=1, blank=True)
    seRelaciona = models.CharField(max_length=1, blank=True)

#     Aspecto Intelectual

    pronuciaCorretamente = models.CharField(max_length=1, blank=True)
    expressaPensanetos = models.CharField(max_length=1, blank=True)
    transmiteRecados = models.CharField(max_length=1, blank=True)
    fazPedido = models.CharField(max_length=1, blank=True)

    descricaoUsuario = models.TextField(blank=True)
    pessoaQuestionada = models.CharField(max_length=50, blank=True)





