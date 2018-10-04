from django.shortcuts import render
from .models import *
# Create your views here.

def index(request):
	return render(request, 'pedagogico/index.html', {})

def criar_turma(request):
	professores = Funcionario.objects.all()
	return render(request, 'pedagogico/criar_turma.html', {"professores":professores})

def cadastrar_aula(request):
    turmas = Turma.objects.all()
    aulas = Aula.objects.all()
    return render(request, 'pedagogico/cadastrar_aula.html', {"turmas":turmas, "aulas":aulas})

def frequencia(request):
    turmas = Turma.objects.all()
    usuarios = Usuario.objects.all()
    aulas = Aula.objects.all()
    return render(request, 'pedagogico/frequencia.html', {"usuarios":usuarios, "turmas":turmas, "aulas":aulas})

def triagem_pedagogica(request):
    return render(request, 'pedagogico/triagem_pedagogica.html')