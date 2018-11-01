from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
# from django.views.generic import CreateView, FormView

from django.views import generic

from social.models import *
from core.models import *

import datetime



# Views
@login_required
def index(request):
    dados = {}
    
    return render(request,'social/index.html', dados)

#----------------------------------------------------------------------------------------
#Views da Triagem
@login_required
def triagem_realizar(request):
    cids= CID.objects.all()
    args = {'cids':cids, "e":'{', 'd':'}'}
    return render(request,'social/triagem_realizar.html', args)

@login_required
def triagem_editar(request,triagem_id):
    t = get_object_or_404(Triagem,pk=triagem_id)
    return render(request,'social/triagem_editar.html', {'t':t})

@login_required
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




#--------------------------------------------------------------------------------------------
#Views do usuario
@login_required
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
@login_required
def visita_agendar(request,usuario_id):
    return render(request,'social/visita_agendar.html', {})

@login_required
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

#---------------------------------------------------------------------------------------------------------------
#controle de Tricagem
@login_required
def cadastrar_triagem(request):
    
    cid = CID.objects.get(codigo=request.POST['cid'])
    usuario = Usuario(nome=request.POST['nome'], cid=cid)

    try:
        data = request.POST['datanascimento']
        data = data.split('/')

        datanascimento = datetime.datetime(int(data[2]),int(data[1]),int(data[0]))
        usuario.data_nacimento = datanascimento
    except Exception as e:
        datanascimento = datetime.datetime(2000,1,1)
        usuario.data_nacimento = datanascimento

    try:
        usuario.imagem = request.FILES['imagem']   
    except Exception as e:
        pass

    
    triagem = Triagem()

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
    # funcionario = Funcionario(nome= request.POST['assinatura'])
    # funcionario.save()
    funcionario = request.user.funcionario
    triagem.assinatura_proficinal = funcionario
    
    data = request.POST['datarealizacao']
    data = data.split(' ')

    data[0] = data[0].split('/')
    data[1] = data[1].split(':')

    datatriagem = datetime.datetime(int(data[0][2]),int(data[0][1]),int(data[0][0]))
    datatriagem.replace(hour=int(data[1][0]),minute=int(data[1][1]),second=int(data[1][2]))

    triagem.data_da_triagem = datatriagem

    usuario.save()
    triagem.usuario = usuario
    triagem.save()

    return HttpResponseRedirect(reverse('social:triagem_editar', args=(triagem.id,)))


@login_required
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

#----------------------------------------------------------------------------------------------------
#Eventos
@login_required
def evento_cadastrar(request):

    if "nome" in request.POST:
        data = request.POST['datainicio']
        data = data.split('/')
        dataa = data[2]+"-"+data[1]+"-"+data[0]

        data = request.POST['datafim']
        data = data.split('/')
        datab = data[2]+"-"+data[1]+"-"+data[0]

    
        e = Evento(nome = request.POST['nome'], data_inicio = dataa, data_fim = datab)
        e.save()
        return HttpResponseRedirect(reverse('social:index' ))
    return render(request,'social/evento_cadastrar.html',{})



class Test_view_generica(generic.ListView):
    template_name = 'social/test.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        """Return the last five published questions."""
        return Usuario.objects.all()


class Test_view_generica_a(generic.DetailView):
    model = Usuario
    template_name = 'social/testa.html'