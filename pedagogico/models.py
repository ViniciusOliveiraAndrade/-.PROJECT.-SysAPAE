from django.db import models
from core.models import *
# Create your models here.

class Turma(models.Model):
    nome = models.CharField(max_length=50)
    turno = models.BooleanField()

    def __str__(self):
        return "Turma: "+self.nome

class Aula(models.Model):
    data = models.DateTimeField('Data da Aula')
    conteudo = models.CharField(max_length=500)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)


class Frequencia(models.Model):
    dataFrequencia = models.DateTimeField('Data da Frequencia', null=True, blank=True)
    presente = models.BooleanField()
    abono = models.BooleanField()
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)


class UsuarioTurma(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

class ProfessorTurma(models.Model):
    professor = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)


class TriagemPedagogica(models.Model):
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
    fazBarulho = models.BooleanField()

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




