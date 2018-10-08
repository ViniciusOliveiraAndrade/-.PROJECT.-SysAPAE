from django.shortcuts import render
from .models import *


# Create your views here.

def index(request):
    return render(request, 'pedagogico/index.html', {})


def criar_turma(request):
    professores = Funcionario.objects.all()
    return render(request, 'pedagogico/criar_turma.html', {"professores": professores})


def cadastrar_aula(request):
    turmas = Turma.objects.all()
    aulas = Aula.objects.all()
    usuarioTurma = UsuarioTurma.objects.all()
    return render(request, 'pedagogico/cadastrar_aula.html',
                  {"turmas": turmas, "aulas": aulas, "usuarioTurma": usuarioTurma})


def frequencia(request):
    turmas = Turma.objects.all()
    usuarios = Usuario.objects.all()
    aulas = Aula.objects.all()
    return render(request, 'pedagogico/frequencia.html', {"usuarios": usuarios, "turmas": turmas, "aulas": aulas})


def triagem_pedagogica(request):
    return render(request, 'pedagogico/triagem_pedagogica.html')


def cadastrar_turmas(request):
    professor = Funcionario.objects.get(nome=request.POST["professor"])

    if request.POST['turno'] == "tarde":
        turno = False
    else:
        turno = True

    turma = Turma(nome=request.POST['nome'], turno=turno);
    turma.save()
    protuma = ProfessorTurma(professor=professor, turma=turma)
    protuma.save()
    return render(request, 'pedagogico/index.html')

    print("veioaqui")
    print(request.POST)

def cadastrar_aulas(resquest):
    turma = Turma.objects.get(nomeTurma=resquest.POST["turma"])
    turma.save()
    data = Aula.objects.get(data=resquest.POST["data"])
    data.save()
    conteudo = Aula.objects.get(conteudo=resquest.POST["conteudo"])
    conteudo.save()

    aulaSalva = Aula(data=data, nomeTurma=turma, conteudo=conteudo)
    aulaSalva.save()

    return render(resquest, 'pedagogico/index.html')
