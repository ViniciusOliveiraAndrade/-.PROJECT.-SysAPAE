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
    args = {'cids':cids}
    return render(request,'social/triagem_realizar.html', args)

@login_required
def triagem_editar(request,triagem_id):
    t = get_object_or_404(Triagem,pk=triagem_id)
    cids= CID.objects.all()
    args = {'cids':cids, 't':t}
    return render(request,'social/triagem_editar.html', args)

@login_required
def triagem_detalhe(request,triagem_id):
    t = get_object_or_404(Triagem,pk=triagem_id)
    return render(request,'social/triagem_detalhe.html', {'t':t})

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
    gerar_acao(request.user.funcionario,"Cadastro","Triagem",triagem.id)
    return HttpResponseRedirect(reverse('social:triagem_editar', args=(triagem.id,)))

@login_required
def editar_triagem(request):

    triagem = get_object_or_404(Triagem,pk=request.POST['id'])

    data = request.POST['datanascimento']
    data = data.split('/')
    datanascimento = datetime.datetime(int(data[2]),int(data[1]),int(data[0]))

    triagem.usuario.nome=request.POST['nome']
    cid = CID.objects.get(codigo=request.POST['cid'])
    triagem.usuario.cid=cid
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
    triagem.save()
    gerar_acao(request.user.funcionario,"Edição","Triagem",triagem.id)
    return triagem_editar(request,triagem.id)

#--------------------------------------------------------------------------------------------
#Views do usuario
@login_required
def usuarios_listar(request):
    

    try:
        triagens = Triagem.objects.filter(usuario__situacao="Ativo")
    except Exception as e:
        u = Usuario()
        f = Funcionario()
        t = Triagem()
        t.usuario = u
        t.assinatura_proficinal = f
        triagens = [t]
        raise e
    if request.method == 'POST':
        u = get_object_or_404(Usuario,pk=request.POST['id'])
        u.situacao = "Inativo"
        u.save()
        gerar_acao(request.user.funcionario,"Inativar","Usuario",u.id)
        return redirect("social:usuarios_listar")

    return render(request,'social/usuario_listar.html', {'triagens' : triagens})

#--------------------------------------------------------------------------------------------
#views da visita
@login_required
def visita_agendar(request,usuario_id):
    u = Usuario.objects.get(pk=usuario_id)
    f = Funcionario.objects.filter(cargo__nome="Assistente social")

    if request.method == "POST":
        
        usuario = Usuario.objects.get(pk=request.POST['usuario_id'])
        
        first_name, last_name = getNomeFuncionario(request.POST['funcionario'])
        print(getNomeFuncionario(request.POST['funcionario']))
        funcionario = Funcionario.objects.get(user__first_name=first_name, user__last_name=last_name)
        
        try:
            data = request.POST['datavisita']
            print(data)
            data = data.split('/')

            datavisita = datetime.datetime(int(data[2]),int(data[1]),int(data[0]))
        except Exception as e:
            datavisita = datetime.datetime(2000,1,1)

        if request.POST['realizada'] == 'Sim':
            realizada = True
        else:
            realizada = False

        observacoes = request.POST['obs']

        visita = Visita.objects.create(
            usuario=usuario,
            funcionario=funcionario,
            data_visita=datavisita,
            observacoes=observacoes,
            realizada=realizada
            )

        gerar_acao(request.user.funcionario,"Cadastro","Visita",visita.id)
        return HttpResponseRedirect(reverse('social:visita_editar', args=(visita.id,)))

    return render(request,'social/visita_agendar.html', {'usuario':u, 'funcionario':f})

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

@login_required
def visita_editar(request,visita_id):
    try:
        visita = Visita.objects.get(pk=visita_id)
    except Exception as e:
        visitas = {}
        raise e

    return render(request,'social/visita_listar.html', {'visitas' : visitas})

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
        gerar_acao(request.user.funcionario,"Cadastro","Evento",e.id)
        return HttpResponseRedirect(reverse('social:index' ))
    return render(request,'social/evento_cadastrar.html',{})

def gerar_acao(user,tipo_acao,dado_acao,iddado):
    Registro_acao.objects.create(usuario=user,tipo=tipo_acao,dado=dado_acao, id_dado=iddado)

def getNomeFuncionario(requestPost):
    nome_funcionario = requestPost
    nome_funcionario = nome_funcionario.split(' ')
    first_name = nome_funcionario[0]
    last_name = " ".join(nome_funcionario[1:])
    return first_name, last_name
