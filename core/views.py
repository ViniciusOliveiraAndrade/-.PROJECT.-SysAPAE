from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
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


def verilicar_logado(request):
	if not request.user.is_authenticated:
		return render(request, 'core:login')