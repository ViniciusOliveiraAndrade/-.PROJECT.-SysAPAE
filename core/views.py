from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as login_f, logout as logout_f
from django.contrib.auth.decorators import login_required
from core.models import *

# Create your views here.
@login_required
def index(request):
    dados = {'request':request}
    
    return render(request,'core/index.html', dados)


def registrar(request):
    if request.method == "POST":
    	form = UserCreationForm(request.POST)
    	if form.is_valid:
    		form.save()
    		return redirect('core:index')
    else:
    	form = UserCreationForm()
    	return render(request,'core/registrar.html',{"form":form})



def cadastrar_funcionario(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('core:index')
    else:
        form = UserCreationForm()
        return render(request,'core/registrar.html',{"form":form})    


def login(request):
    #ja verifica se tem dados no banco de dados e se não cria dados base
    if CID.objects.all().count() == 0:
        criar_dados()

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login_f(request, user)
            Registro_acesso.objects.create(usuario=user.funcionario)
            #Já verifica o cargo e direciona para o local correto 
            if user.funcionario.cargo.nome == "Coordenador(a) pedagógica" or user.funcionario.cargo.nome == "Educador(a)": 
                return redirect('pedagogico:index')
            else:
                return redirect('social:index')
        else:
            return render(request,'core/login.html',{'erro':True})
            
    else:
        if not request.user.is_authenticated:
            return render(request,'core/login.html')
        else:
            return redirect('core:index')

def logout(request):
    logout_f(request)
    return render(request,'core/logout.html')
    

