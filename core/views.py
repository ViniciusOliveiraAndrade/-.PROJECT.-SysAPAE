from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as login_f, logout as logout_f
from django.contrib.auth.decorators import login_required
from core.models import *

from core.utilidades import *

# Create your views here.
@login_required
def index(request):
    if request.user.funcionario.cargo.nome == "Coordenador(a) pedagógica" or request.user.funcionario.cargo.nome == "Educador(a)": 
        return redirect('pedagogico:index')
    else:
        return redirect('social:index')

    return render(request,'core/index.html', dados)

@login_required
def registrarFuncionario(request):
    if request.method == "POST":
    	
        user = User.objects.create_user(request.POST['nomeuser'], request.POST['email'], '123456Mm')
        pnome, unome = getNomeFuncionario(request.POST['nome'])
        user.first_name = pnome
        user.last_name = unome
        user.save()
        cargo = Cargo.objects.get(nome=request.POST['cargo'])

        Funcionario.objects.create(user=user, cargo=cargo)
        return redirect('core:index')
        
         
    else:
    	cargos = Cargo.objects.all()
    	return render(request,'core/registrar.html',{'cargos':cargos})
 

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
@login_required
def logout(request):
    logout_f(request)
    return render(request,'core/logout.html')

@login_required   
def registro(request):
    acessos = Registro_acesso.objects.all().order_by('-data_acesso')
    acoes = Registro_acao.objects.all().order_by('-data_acao')
    dados = {"acessos":acessos, "acoes":acoes}
    return render(request,'core/registro.html',dados)

@login_required
def help(request):
    
    dados = {}
    return render(request,'core/help.html',dados)
