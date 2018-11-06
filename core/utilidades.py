from django.shortcuts import redirect

from core.models import *

import datetime

def gerar_acao(user,tipo_acao,dado_acao,iddado):
    Registro_acao.objects.create(usuario=user,tipo=tipo_acao,dado=dado_acao, id_dado=iddado)

def getNomeFuncionario(requestPost):
    nome_funcionario = requestPost
    nome_funcionario = nome_funcionario.split(' ')
    first_name = nome_funcionario[0]
    last_name = " ".join(nome_funcionario[1:])
    return first_name, last_name

def restringir_pedagogico(request):
	if request.user.funcionario.cargo.nome == "Coordenador(a) social" or request.user.funcionario.cargo.nome == "Assistente social":
		return redirect('social:index')
		

def restringir_social(request):
    if request.user.funcionario.cargo.nome == "Coordenador(a) pedagógica" or request.user.funcionario.cargo.nome == "Educador(a)":
        return redirect('pedagogico:index')

def criar_dados():
    #criar cargos
    cargo1 = Cargo.objects.create(nome = "Coordenador(a) pedagógica")
    
    cargo2 = Cargo.objects.create(nome = "Educador(a)")
    
    cargo3 = Cargo.objects.create(nome = "Coordenador(a) social")

    cargo4 = Cargo.objects.create(nome = "Assistente social")

    #Criar usuarios e os funcionarios
    user1 = User.objects.create_user('ednaele', 'ednaele@apae.com', '123456Mm')
    user1.first_name = "Ednaele"
    user1.last_name = "de alguma coisa"
    user1.save()
    funcionario1 = Funcionario.objects.create(user=user1, cargo=cargo1)

    user2 = User.objects.create_user('cintia', 'cintia@apae.com', '123456Mm')
    user2.first_name = "Cintia"
    user2.last_name = "de alguma coisa"
    user2.save()
    funcionario2 = Funcionario.objects.create(user=user2, cargo=cargo2)
    
    user3 = User.objects.create_user('marilia', 'marilia@apae.com', '123456Mm')
    user3.first_name = "Marília"
    user3.last_name = "de alguma coisa"
    user3.save()
    funcionario3 = Funcionario.objects.create(user=user3, cargo=cargo3)

    user4 = User.objects.create_user('juliana', 'juliana@apae.com', '123456Mm')
    user4.first_name = "Juliana"
    user4.last_name = "de alguma coisa"
    user4.save()
    funcionario4 = Funcionario.objects.create(user=user4, cargo=cargo4)

    #Criar as CID
    cid = CID.objects.create(codigo="F00",descricao="Demência na Doença de Alzheimer")
    cid = CID.objects.create(codigo="F01",descricao="Demência Vascular")
    cid = CID.objects.create(codigo="F02",descricao="Demência em Outras Doenças Classificadas em Outra Parte")
    cid = CID.objects.create(codigo="F03",descricao="Demência Não Especificada")
    cid = CID.objects.create(codigo="F04",descricao="Síndrome Amnésica Orgânica Não Induzida Pelo Álcool ou Por Outras Substâncias Psicoativas")
    cid = CID.objects.create(codigo="F05",descricao="Delirium Não Induzido Pelo Álcool ou Por Outras Substâncias Psicoativas")
    cid = CID.objects.create(codigo="F06",descricao="Outros Transtornos Mentais Devidos a Lesão e Disfunção Cerebral e a Doença Física")
    cid = CID.objects.create(codigo="F07",descricao="Transtornos de Personalidade e do Comportamento Devidos a Doença, a Lesão e a Disfunção Cerebral")
    cid = CID.objects.create(codigo="F08",descricao="Transtorno Mental Orgânico ou Sintomático Não Especificado")
    cid = CID.objects.create(codigo="F09",descricao="Transtornos Mentais e Comportamentais Devidos ao Uso de Álcool")
    cid = CID.objects.create(codigo="F10",descricao="Transtornos Mentais e Comportamentais Devidos ao Uso de Opiáceos")
    cid = CID.objects.create(codigo="F11",descricao="Transtornos Mentais e Comportamentais Devidos ao Uso de Canabinóides")

def getData_inputDate(requestPost):
    try:
        data = requestPost
        data = data.split('-')
        dataRetorno = datetime.datetime(int(data[0]),int(data[1]),int(data[2]))
    except Exception as e:
        dataRetorno = datetime.datetime(2000,1,1)
    return dataRetorno