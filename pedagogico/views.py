from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from .models import *
from social.models import Triagem
import datetime


# Create your views here.

# --------------------------------------- | TELAS | ---------------------------------------

def index(request):
    return render(request, 'pedagogico/index.html', {})


def criar_turma(request):
    professores = Funcionario.objects.all()

    so_professor = []

    for professor in professores:
        if professor.cargo.nome == "Professor":
            so_professor.append(professor)

    return render(request, 'pedagogico/criar_turmaCoordenacao.html', {"professores": so_professor})


def cadastrar_aula(request, id_turma):
    # usuarioTurma = UsuarioTurma.objects.all()
    return render(request, 'pedagogico/cadastrar_aula.html', {"turma": id_turma })


def frequencia(request, id_aula):
    usuarios = Usuario.objects.all()

    # aula = Turma.objects.get(Turma, pk=id_aula)

    # aulas = Aula.objects.all()

    triagens = Triagem.objects.all()

    return render(request, 'pedagogico/frequencia.html', {"usuarios": usuarios})


def triagem_pedagogica(request, id_usuario):
    u = get_object_or_404(Usuario, pk=id_usuario)
    return render(request, 'pedagogico/triagem_pedagogica.html', {"usuario": u})

def cadastrar_triagemP(request):
    dataTriagem = request.POST['data']

    data = dataTriagem.split('/')
    # datanascimento = datetime.datetime(int(data[2]), int(data[1]), int(data[0]))

    triagemP = TriagemPedagogica()


def listar_triagemSocial(request):
    usuarios = Usuario.objects.all()

    return render(request, 'pedagogico/listar_triagemSocial.html', {"usuarios": usuarios})


def listar_turmas(request):
    listaTurmas = Turma.objects.all()
    return render(request, 'pedagogico/listar_turmasCordenacao.html', {"listaTurmas": listaTurmas})

def listar_aulas(request, id_turma):
    aulas = Turma.objects.get(pk=id_turma).aula.all()
    return render(request, 'pedagogico/listar_aulas.html', {"aulas": aulas, 'id_turma':id_turma})

def listas_turmasProf(request):
    turmas = Turma.objects.all()

    return render(request, "pedagogico/listar_turmasProf.html", {"turmas":turmas})


# --------------------------------------- | METÒDOS | ---------------------------------------

def cadastrar_turmas(request):
    if request.POST['turno'] == "tarde":
        turno = False
    else:
        turno = True

    turma = Turma(nome=request.POST['nome'], turno=turno, professor=Funcionario.objects.get(nome=request.POST["professor"]));
    turma.save()

    return HttpResponseRedirect(reverse('pedagogico:listar_turmas'))


def cadastrar_aulas(request):
    data = request.POST['dataAula']
    data = data.split('-')

    dataAula = datetime.datetime(int(data[0]), int(data[1]), int(data[2]))

    if request.POST["situacao"] == "aberto":
        situacao = True
    else:
        situacao = False

    frequencia = Frequencia.objects.create()
    aula = Aula.objects.create(data=dataAula, situacao=situacao, conteudo=request.POST["conteudo"], titulo=request.POST["tituloAula"],frequencia=frequencia)
    turma = Turma.objects.get(pk=request.POST['id_turma'])
    turma.aula.add(aula)
    turma.save()

    return HttpResponseRedirect(reverse('pedagogico:listar_aulas',args=(turma.id,)))


def editar_aulas(request, id_aula):
    aula = get_object_or_404(Aula, pk=id_aula)

    if "tituloAula" in request.POST:
        aula = get_object_or_404(Aula, pk=request.POST['id'])
        data = request.POST['dataAula']
        data = data.split('/')
        dataa = data[2] + "-" + data[1] + "-" + data[0]

        if request.POST["situacao"] == "aberto":
            situacao = True
        else:
            situacao = False

        aula.data = dataa
        aula.situacao = situacao
        aula.conteudo = request.POST["conteudo"]
        aula.titulo = request.POST["tituloAula"]

        aula.turma = Turma.objects.get(nome=request.POST['turma'])

        aula.save()
        return HttpResponseRedirect(reverse('pedagogico:listar_aulas'))
    return render(request, "pedagogico/editar_aula.html", {"aula": aula})

def editar_turma(request, id_turma):
    turma = get_object_or_404(Turma, pk=id_turma)
    professores = Funcionario.objects.all()

    so_professor = []

    for professor in professores:
        if professor.cargo.nome == "Professor":
            so_professor.append(professor)

    if "nome" in request.POST:
        turma.nome = request.POST['nome']
        turma.professor = get_object_or_404(Funcionario, nome=request.POST['professor'])

        if request.POST['turno'] == "tarde":
            turno = False
        else:
            turno = True

        turma.turno = turno
        turma.save()

        return HttpResponseRedirect(reverse('pedagogico:listar_turmas'))
    return render(request, "pedagogico/editar_turmaCoordenacao.html", {"turma":turma, "professores":so_professor})

def deletar_turma(request, id_turma):
    turma = get_object_or_404(Turma, pk=id_turma)
    turma.delete()
    listaTurmas = Turma.objects.all()
    return HttpResponseRedirect(reverse('pedagogico:listar_turmas'))

def deletar_aula(request, id_aula):
    aula = get_object_or_404(Aula, pk=id_aula)
    aula.delete()

    return HttpResponseRedirect(reverse('pedagogico:listar_aulas'))
