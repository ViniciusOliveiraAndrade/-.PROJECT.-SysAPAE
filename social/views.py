from django import forms
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy, reverse
# from django.views.generic import CreateView, FormView

from django.views import generic

from social.models import Usuario, Funcionario, Triagem, Visita
from core.models import *

import datetime



# Views
def index(request):
    dados = {}
    
    return render(request,'social/index.html', dados)

#
#Views da Triagem
#
def triagem_realizar(request):
    return render(request,'social/triagem_realizar.html', {})


def triagem_editar(request,triagem_id):
    t = get_object_or_404(Triagem,pk=triagem_id)
    return render(request,'social/triagem_editar.html', {'t':t})

def triagem_listar(request):
    try:
        triagens = Triagem.objects.all()
    except Exception as e:
        u = Usuario()
        f = Funcionario()
        t = Triagem()
        t.usuario = u
        t.assinatura_proficinal = f
        triagens = [t]
        raise e

    return render(request,'social/triagem_listar.html', {'triagens' : triagens})

#
#Views do usuario
#
def usuarios_listar(request,delete=False,id=0):
    try:
        triagens = Triagem.objects.all()
    except Exception as e:
        u = Usuario()
        f = Funcionario()
        t = Triagem()
        t.usuario = u
        t.assinatura_proficinal = f
        triagens = [t]
        raise e
    if "delete" in request.GET:
        u = get_object_or_404(Usuario,pk=request.GET['id'])
        u.delete()

    return render(request,'social/usuario_listar.html', {'triagens' : triagens})



#
#views da visita
#
def visita_agendar(request,usuario_id):
    return render(request,'social/visita_agendar.html', {})

def visita_listar(request):
    try:
        visitas = Visita.objects.all()
    except Exception as e:
        u = Usuario()
        f = Funcionario()
        v = Visita()
        v.usuario = u
        v.funcionario = f
        visitas = [v]
        raise e

    return render(request,'social/visita_listar.html', {'visitas' : visitas})


#controle de Tricagem
def cadastrar_triagem(request):
    data = request.POST['datanascimento']
    data = data.split('/')

    datanascimento = datetime.datetime(int(data[2]),int(data[1]),int(data[0]))
    usuario = Usuario(nome=request.POST['nome'], cid=request.POST['cid'], data_nacimento=datanascimento, imagem=request.FILES['imagem'])
    usuario.save()

    triagem = Triagem()
    triagem.usuario = usuario
    triagem.sus = request.POST['sus']
    
    #Especialista
    if request.POST['exampleRadios'] == 'n':
        triagem.acompanhamento_com_especialista = False
    else:
        triagem.acompanhamento_com_especialista = True

    triagem.especialista = request.POST['especialista']
    
    #Familiares
    triagem.nome_pai = request.POST['painome']
    triagem.idade_pai = request.POST['paiidade']
    triagem.profissao_pai = request.POST['paiprofissao']
    
    triagem.nome_mae = request.POST['maenome']
    triagem.idade_mae = request.POST['maeidade']
    triagem.profissao_mae = request.POST['maeprofissao']

    #Renda Familiar
    if 'bpc' not in request.POST:
        triagem.bpc = False
    else:
        triagem.bpc = True

    if 'bolsafamilia' not in request.POST:
        triagem.bolsa_familia = False
    else:
        triagem.bolsa_familia = True

    if 'aposentadoria' not in request.POST:
        triagem.aposentadoria = False
    else:
        triagem.aposentadoria = True

    triagem.renda_familiar = request.POST['valor']
    triagem.benediciario = request.POST['beneficiario']

    #Endereco
    triagem.rua = request.POST['rua']
    triagem.numero_da_rua = request.POST['numero']
    triagem.bairro = request.POST['bairro']
    triagem.ponto_de_referencia = request.POST['ponto']
    triagem.cidade = request.POST['cidade']
    
    #Contato
    triagem.telefone = request.POST['telefone']
    triagem.celular = request.POST['celular']
    triagem.email = request.POST['email']

    #Ensino
    if request.POST['inlineRadioOptions'] == 'n':
        triagem.estuda_ensino_regular = False
    else:
        triagem.estuda_ensino_regular = True
    triagem.qual = request.POST['qual']
    triagem.ano_estuda = request.POST['ano']
    triagem.turma_estuda = request.POST['turma']
    triagem.turno_estuda = request.POST['turno']

    #Observacoes
    triagem.observacoes = request.POST['obs']
    funcionario = Funcionario(nome= request.POST['assinatura'], cargo= "Assistente Social")
    funcionario.save()
    triagem.assinatura_proficinal = funcionario
    
    data = request.POST['datarealizacao']
    data = data.split(' ')

    data[0] = data[0].split('/')
    data[1] = data[1].split(':')



    datatriagem = datetime.datetime(int(data[0][2]),int(data[0][1]),int(data[0][0]))
    datatriagem.replace(hour=int(data[1][0]),minute=int(data[1][1]),second=int(data[1][2]))


    triagem.data_da_triagem = datatriagem
    triagem.save()
    return triagem_editar(request,triagem.id)

def editar_triagem(request):

    triagem = get_object_or_404(Triagem,pk=request.POST['id'])

    data = request.POST['datanascimento']
    data = data.split('/')
    datanascimento = datetime.datetime(int(data[2]),int(data[1]),int(data[0]))

    triagem.usuario.nome=request.POST['nome']
    triagem.usuario.cid=request.POST['cid']
    triagem.usuario.data_nacimento=datanascimento
    triagem.usuario.save()

    
    triagem.sus = request.POST['sus']
    
    #Especialista
    if request.POST['exampleRadios'] == 'n':
        triagem.acompanhamento_com_especialista = False
    else:
        triagem.acompanhamento_com_especialista = True

    triagem.especialista = request.POST['especialista']
    
    #Familiares
    triagem.nome_pai = request.POST['painome']
    triagem.idade_pai = request.POST['paiidade']
    triagem.profissao_pai = request.POST['paiprofissao']
    
    triagem.nome_mae = request.POST['maenome']
    triagem.idade_mae = request.POST['maeidade']
    triagem.profissao_mae = request.POST['maeprofissao']

    #Renda Familiar
    if 'bpc' not in request.POST:
        triagem.bpc = False
    else:
        triagem.bpc = True

    if 'bolsafamilia' not in request.POST:
        triagem.bolsa_familia = False
    else:
        triagem.bolsa_familia = True

    if 'aposentadoria' not in request.POST:
        triagem.aposentadoria = False
    else:
        triagem.aposentadoria = True

    triagem.renda_familiar = request.POST['valor']
    triagem.benediciario = request.POST['beneficiario']

    #Endereco
    triagem.rua = request.POST['rua']
    triagem.numero_da_rua = request.POST['numero']
    triagem.bairro = request.POST['bairro']
    triagem.ponto_de_referencia = request.POST['ponto']
    triagem.cidade = request.POST['cidade']
    
    #Contato
    triagem.telefone = request.POST['telefone']
    triagem.celular = request.POST['celular']
    triagem.email = request.POST['email']

    #Ensino
    if request.POST['inlineRadioOptions'] == 'n':
        triagem.estuda_ensino_regular = False
    else:
        triagem.estuda_ensino_regular = True
    triagem.qual = request.POST['qual']
    triagem.ano_estuda = request.POST['ano']
    triagem.turma_estuda = request.POST['turma']
    triagem.turno_estuda = request.POST['turno']

    #Observacoes
    triagem.observacoes = request.POST['obs']
    triagem.assinatura_proficinal.nome = request.POST['assinatura']
    triagem.assinatura_proficinal.save()
    
    data = request.POST['datarealizacao']
    data = data.split('/')

    datatriagem = datetime.datetime(int(data[2]),int(data[1]),int(data[0]))
    


    triagem.data_da_triagem = datatriagem
    triagem.save()
    return triagem_editar(request,triagem.id)


class Test_view_generica(generic.ListView):
    template_name = 'social/test.html'
    context_object_name = 'all user'

    def get_queryset(self):
        """Return the last five published questions."""
        return Visita.objects.order_by('-realizada')[:5]

class Test_view_generica_a(generic.DetailView):
    model = Usuario
    template_name = 'social/testa.html'