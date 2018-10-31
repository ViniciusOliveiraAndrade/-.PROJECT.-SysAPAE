from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as login_f, logout as logout_f
from django.contrib.auth.decorators import login_required

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


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login_f(request, user)
            return redirect('core:index')
        else:
            return render(request,'core/login.html',{'erro':True})
            
    else:
        return render(request,'core/login.html')

def logout(request):
    logout_f(request)
    return render(request,'core/logout.html')
    