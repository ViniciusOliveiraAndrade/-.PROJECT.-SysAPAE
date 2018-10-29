from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from .models import *
from social.models import Triagem


# Create your views here.

def index(request):
    return render(request, 'pedagogico/index.html', {})


def criar_turma(request):
    professores = Funcionario.objects.all()

    so_professor = []

    for professor in professores:
        if professor.cargo.descricao == "Professor":
            so_professor.append(professor)

    return render(request, 'pedagogico/criar_turma.html', {"professores": so_professor})


def cadastrar_aula(request):
    turmas = Turma.objects.all()
    aulas = Aula.objects.all()
    # usuarioTurma = UsuarioTurma.objects.all()
    return render(request, 'pedagogico/cadastrar_aula.html',
                  {"turmas": turmas, "aulas": aulas})


def frequencia(request):
    turmas = Turma.objects.all()
    usuarios = Usuario.objects.all()

    aulas = Aula.objects.all()

    triagens = Triagem.objects.all()

    return render(request, 'pedagogico/frequencia.html', {"usuarios": usuarios, "turmas": turmas, "aulas": aulas})


def triagem_pedagogica(request, id_usuario):
    u = get_object_or_404(Usuario, pk=id_usuario)
    return render(request, 'pedagogico/triagem_pedagogica.html', {"usuario": u})

def cadastrar_triagemP(request):
    dataTriagem = request.POST['data']

    data = dataTriagem.split('/')
    # datanascimento = datetime.datetime(int(data[2]), int(data[1]), int(data[0]))

    triagemP = TriagemPedagogica()

def cadastrar_turmas(request):
    nomesP = request.POST["professor"]

    nomesP = nomesP.split(',')

    profesorres = []
    for nome in nomesP:
        print(nome)
        professor = Funcionario.objects.get(nome=nome)
        profesorres.append(professor)

    if request.POST['turno'] == "tarde":
        turno = False
    else:
        turno = True

    turma = Turma(nome=request.POST['nome'], turno=turno);
    turma.save()

    for professor in profesorres:
        print(professor.nome)
        turma.professor.add(professor)

    return render(request, 'pedagogico/criar_turma.html')


def cadastrar_aulas(resquest):
    if "conteudo" in resquest.POST:
        data = resquest.POST['dataAula']
        data = data.split('/')
        dataa = data[2] + "-" + data[1] + "-" + data[0]


        if resquest.POST["situacao"] == "aberto":
            situacao = True
        else:
            situacao = False

        aula = Aula(data=dataa, situacao=situacao, conteudo=resquest.POST["conteudo"], titulo=resquest.POST["tituloAula"])

        aula.turma = Turma.objects.get(nome=resquest.POST['turma'])
        aula.save()

        return HttpResponseRedirect(reverse('pedagogico:cadastrar_aula'))
    return render(resquest, 'pedagogico/cadastrar_aula.html')


def listar_triagemSocial(request):
    usuarios = Usuario.objects.all()

    return render(request, 'pedagogico/listar_triagemSocial.html', {"usuarios": usuarios})


def listar_turmas(request):
    listaTurmas = Turma.objects.all()
    return render(request, 'pedagogico/listar_turmas.html', {"listaTurmas": listaTurmas})

def listar_aulas(request):
    aulas = Aula.objects.all()
    return render(request, 'pedagogico/listar_aulas.html', {"aulas": aulas})

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
        return HttpResponseRedirect(reverse('pedagogico:index'))
    return render(request, "pedagogico/editar_aula.html", {"aula": aula})

def editar_turma(request, id_turma):
    turma = get_object_or_404(Turma, pk=id_turma)
    professores = Funcionario.objects.all()

    so_professor = []

    for professor in professores:
        if professor.cargo.descricao == "Professor":
            so_professor.append(professor)
    #
    # if "nome" in request.POST:
    #     turma.nome = request.POST['nome']
    #     turma.professor = get_object_or_404(Funcionario, )

    return render(request, "pedagogico/editar_turma.html", {"turma":turma, "professores":so_professor})

def deletar_turma(request, id_turma):
    turma = get_object_or_404(Turma, pk=id_turma)
    turma.delete()
    listaTurmas = Turma.objects.all()
    return HttpResponseRedirect(reverse('pedagogico:listar_turmas'))

def deletar_aula(request, id_aula):
    aula = get_object_or_404(Aula, pk=id_aula)
    aula.delete()

    return HttpResponseRedirect(reverse('pedagogico:listar_aulas'))