from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy, reverse

from django.utils.dateparse import parse_time

from core.utilidades import *
from .models import *
from social.models import Triagem
import datetime
import core.utilidades


# Create your views here.

# --------------------------------------- | TELAS | ---------------------------------------
@login_required
def index(request):
    return render(request, 'pedagogico/index.html', {})

@login_required
def perfil(request):
    if request.method == "POST":
        if request.POST['verificaimagem'] != "Sem Imagem" and request.POST[
            'verificaimagem'] != request.user.funcionario.imagem_url:
            try:
                request.user.funcionario.imagem.delete(save=True)
                request.user.funcionario.imagem = request.FILES['imagem']
                request.user.funcionario.save()
            except Exception as e:
                pass
        pnome, unome = getNomeFuncionario(request.POST['nome'])
        request.user.first_name = pnome
        request.user.last_name = unome
        request.user.email = request.POST['email']
        request.user.save()
        gerar_acao(request.user.funcionario, "Edição", "Funcionario", request.user.funcionario.id)
    return render(request, 'pedagogico/perfil.html')

@login_required
def criar_turma(request):
    professores = Funcionario.objects.filter(cargo__nome="Educador(a)")
    return render(request, 'pedagogico/criar_turmaCoordenacao.html', {"professores": professores})

@login_required
def cadastrar_aula(request, id_turma):
    return render(request, 'pedagogico/cadastrar_aula.html', {"turma": id_turma})

@login_required
def frequencia(request, id_aula):
    aula = Aula.objects.get(pk=id_aula)

    return render(request, 'pedagogico/frequencia_AlunosEducador.html', {"aula": aula})

@login_required
def frequencia_Coordenacao(request, id_aula):
    aula = Aula.objects.get(pk=id_aula)

    return render(request, 'pedagogico/frequencia_AlunosCoord.html', {"aula": aula})

@login_required
def triagem_pedagogica(request, id_usuario):
    u = get_object_or_404(Triagem, pk=id_usuario)
    turmas = Turma.objects.all()

    return render(request, 'pedagogico/triagem_pedagogica.html', {"Triagem": u, "Turmas": turmas})

@login_required
def cadastrar_triagemP(request):
    dataTriagem = request.POST['data']

    data = dataTriagem.split('/')
    # datanascimento = datetime.datetime(int(data[2]), int(data[1]), int(data[0]))

    triagemP = TriagemPedagogica()

@login_required
def listar_triagemSocial(request):
    triagemSocial = Triagem.objects.filter(usuario__situacao="Ativo").exclude(usuario__triagempedagogica__isnull=False)

    pedagogica_t = TriagemPedagogica.objects.all().order_by('usuario__nome')

    return render(request, 'pedagogico/listar_triagemSocial.html',
                  {"triagemSocial": triagemSocial, "listaPedagogica": pedagogica_t})


@login_required
def listar_turmas(request):
    listaTurmas = Turma.objects.all().order_by('nome')
    return render(request, 'pedagogico/listar_turmasCordenacao.html', {"listaTurmas": listaTurmas})


@login_required
def listar_aulas(request, id_turma):
    aulas = Turma.objects.get(pk=id_turma).aula.all()
    return render(request, 'pedagogico/listar_aulas.html', {"aulas": aulas, 'id_turma': id_turma})


@login_required
def listas_turmasProf(request):
    turmas = request.user.funcionario.turma_set.all()

    return render(request, "pedagogico/listar_turmasProf.html", {"turmas": turmas})


@login_required
def detalhes_aula(request, id_aula):
    id = Aula.objects.get(pk=id_aula)

    return render(request, "pedagogico/aula_detalhes.html", {"idAula": id})


@login_required
def lista_Tpedagogica(request):
    pedagogica_t = TriagemPedagogica.objects.all().order_by('usuario__nome')
    # pedagogica_t = sorted(TriagemPedagogica.usuario.nome)

    return render(request, 'pedagogico/listagem_pedagogica.html', {"listaPedagogica": pedagogica_t})


@login_required
def ver_turmaCoord(request, id_turma):
    turma = Turma.objects.get(pk=id_turma)

    return render(request, 'pedagogico/aulas_turmaCoordenacao.html', {"Turma": turma})


@login_required
def editar_triagem(request, id_triagem):
    triagem = TriagemPedagogica.objects.get(pk=id_triagem)
    turma = Turma.objects.all()

    return render(request, 'pedagogico/editar_triagem.html', {"Triagem": triagem, "Turmas": turma})


@login_required
def detalhes_triagem(request, id_triagem):
    triagem = TriagemPedagogica.objects.get(pk=id_triagem)

    return render(request, 'pedagogico/triagem_detalhes.html', {"Triagem": triagem})


@login_required
def lista_alunos(request, id_turma):
    turma = Turma.objects.get(pk=id_turma)

    return render(request, 'pedagogico/lista_alunosTurma.html', {"Turmas": turma})


@login_required
def realizar_pei(request, id_usuario):
    turma = Turma.objects.get(ususario__id=id_usuario)
    pei = PEI.objects.get(usuario__id=id_usuario, turma=turma)

    return render(request, 'pedagogico/realizar_pei.html', {"PEI": pei})


@login_required
def pei_detalhes(request, id_usuario):
    turma = Turma.objects.get(ususario__id=id_usuario)
    pei = PEI.objects.get(usuario__id=id_usuario, turma=turma)

    return render(request, 'pedagogico/pei_detalhes.html', {"PEI": pei})


@login_required
def editar_pei(request):
    return render(request, 'pedagogico/editar_pei.html')


# --------------------------------------- | METÒDOS | ---------------------------------------

def cadastrar_turmas(request):
    if request.POST['turno'] == "tarde":
        turno = False
    else:
        turno = True

    pnome, snome = getNomeFuncionario(request.POST["professor"])
    professor = Funcionario.objects.get(user__first_name=pnome, user__last_name=snome)
    turma = Turma(nome=request.POST['nome'], turno=turno, professor=professor);
    turma.save()

    return HttpResponseRedirect(reverse('pedagogico:listar_turmas'))


def cadastrar_aulas(request):
    data = request.POST['dataAula']
    data = data.split('-')

    dataAula = datetime.datetime(int(data[0]), int(data[1]), int(data[2]))

    if request.POST["situacao"] == "aberto":
        situacao = True
    else:
        situacao = False

    aula = Aula.objects.create(data=dataAula, situacao=situacao, conteudo=request.POST["conteudo"],
                               titulo=request.POST["tituloAula"])

    turma = Turma.objects.get(pk=request.POST['id_turma'])
    turma.aula.add(aula)

    usuarios = turma.ususario.all()
    for u in usuarios:
        print(u.nome)
        frequencia = Frequencia(falta=False, usuario=u, desempenho="")
        frequencia.save()
        aula.frequencia.add(frequencia)

    aula.save()
    turma.save()

    return HttpResponseRedirect(reverse('pedagogico:listar_aulas', args=(turma.id,)))


def editar_aulas(request, id_aula):
    aula = get_object_or_404(Aula, pk=id_aula)
    if request.method == "POST":
        aula = get_object_or_404(Aula, pk=id_aula)

        if request.POST["situacao"] == "aberto":
            situacao = True
        else:
            situacao = False

        aula.situacao = situacao
        aula.avaliacaoAula = request.POST['avaliacao']
        aula.save()

        turma = aula.turma_set.all()[0:1]
        turma = turma[0]

        return HttpResponseRedirect(reverse('pedagogico:listar_aulas', args=(turma.id,)))
    return render(request, "pedagogico/conclusao_aula.html", {"aula": aula})


def editar_turma(request, id_turma):  # TELA e MEtÓDO tudo ao mesmo tempo
    turma = get_object_or_404(Turma, pk=id_turma)
    professores = Funcionario.objects.filter(cargo__nome="Educador(a)")
    if "nome" in request.POST:
        turma.nome = request.POST['nome']

        pnome, snome = getNomeFuncionario(request.POST["professor"])
        professor = Funcionario.objects.get(user__first_name=pnome, user__last_name=snome)

        turma.professor = professor

        if request.POST['turno'] == "tarde":
            turno = False
        else:
            turno = True

        turma.turno = turno
        turma.save()

        return HttpResponseRedirect(reverse('pedagogico:listar_turmas'))
    return render(request, "pedagogico/editar_turmaCoordenacao.html", {"turma": turma, "professores": professores})


def deletar_turma(request, id_turma):
    turma = get_object_or_404(Turma, pk=id_turma)
    turma.delete()
    listaTurmas = Turma.objects.all()
    return HttpResponseRedirect(reverse('pedagogico:listar_turmas'))


def deletar_aula(request, id_aula):
    aula = get_object_or_404(Aula, pk=id_aula)

    turma = aula.turma_set.all()[0:1]
    turma = turma[0]

    aula.delete()

    return HttpResponseRedirect(reverse('pedagogico:listar_aulas', args=(turma.id,)))


def cadastrarTriagem(request):
    if request.POST['urinario'] == "sim":
        urinario = True
    else:
        urinario = False

    if request.POST['esfincter'] == "sim":
        esfincter = True
    else:
        esfincter = False

    usuarioT = Usuario.objects.get(pk=request.POST['usuario'])

    alimentacao = request.POST['alimentacao']
    cuidador = request.POST['cuidador']
    responsavel = request.POST['responsavel']

    if 'segunda' in request.POST:
        if request.POST['segunda'] == "segunda":
            segunda = True
        else:
            segunda = False
    else:
        segunda = False

    if 'terca' in request.POST:
        if request.POST['terca'] == "terca":
            terca = True
        else:
            terca = False
    else:
        terca = False

    if 'quarta' in request.POST:
        if request.POST['quarta'] == "quarta":
            quarta = True
        else:
            quarta = False
    else:
        quarta = False

    if 'quinta' in request.POST:
        if request.POST['quinta'] == "quinta":
            quinta = True
        else:
            quinta = False
    else:
        quinta = False

    if 'sexta' in request.POST:
        if request.POST['sexta'] == "sexta":
            sexta = True
        else:
            sexta = False
    else:
        sexta = False

    dormeCom = request.POST['dormeCom']
    horaDormir = request.POST['horaDormir']
    horaAcordar = request.POST['horaAcordar']

    horaDormir1 = parse_time(horaDormir)
    horaAcordar1 = parse_time(horaAcordar)

    composicaoFamiliar = request.POST['composicaoFamiliar']
    observacao = request.POST['observacao']

    # .............PEDAGOGICO...........

    musica = request.POST['musica']
    danca = request.POST['danca']
    pintura = request.POST['pintura']
    jiujitsu = request.POST['jiujtso']
    edFisica = request.POST['edFisica']
    informatica = request.POST['informatica']
    robotica = request.POST['robotica']
    teatro = request.POST['teatro']

    # .............ASPECTOS DE DESENVOLVIMENTO...........

    falaBem = request.POST['fala']
    comunicaComGesto = request.POST['gestos']
    ehGago = request.POST['gago']
    enxergaBem = request.POST['enxerga']
    maoDireita = request.POST['direita']
    maoEsquerda = request.POST['esquerda']
    fazBalbucio = request.POST['balbucio']

    # .............ASPECTO FISICO MOTOR...........

    anda = request.POST['anda']
    seguraLapis = request.POST['segura']
    sentaCorretamente = request.POST['senta']
    caiMuito = request.POST['cai']
    cansa = request.POST['cansa']

    # .............ASPECTO EMOCIONAL...........

    demonstraAfeto = request.POST['demonstra']
    solicitaAfeto = request.POST['solicita']
    ehMedroso = request.POST['medroso']
    ehAgressivo = request.POST['agressivo']
    reage = request.POST['reage']
    possuiTique = request.POST['tique']
    choraFacil = request.POST['chora']

    # .............ASPECTO SOCIAL...........

    sabeEsperar = request.POST['espera']
    obedeceOrdens = request.POST['obedece']
    fazAmizades = request.POST['amizades']
    isolase = request.POST['isola']
    sabeDividir = request.POST['divide']
    seRelaciona = request.POST['relaciona']

    # .............ASPECTO INTELECTUAL...........

    pronuciaCorreto = request.POST['pronucia']
    expressaPensamento = request.POST['expressa']
    transmiteRecados = request.POST['recado']
    instrucoes = request.POST['instrucoes']

    descrisaoUsuario = request.POST['descricao']

    data = request.POST['data']
    data = data.split(' ')

    data[0] = data[0].split('/')
    data[1] = data[1].split(':')

    datatriagem = datetime.datetime(int(data[0][2]), int(data[0][1]), int(data[0][0]))
    datatriagem.replace(hour=int(data[1][0]), minute=int(data[1][1]), second=int(data[1][2]))

    dataTriagem = datatriagem

    pessoaQuestionada = request.POST['responsavelTriagem']

    TriagemPedagogica.objects.create(usuario=usuarioT, controleUrinario=urinario,
                                     controleEsfincter=esfincter,
                                     alimentacao=alimentacao, cuidador=cuidador,
                                     responsavel=responsavel, segunda=segunda, terca=terca, quarta=quarta,
                                     quinta=quinta,
                                     sexta=sexta, dormeCom=dormeCom, horarioDormir=horaDormir1,
                                     horarioAcordar=horaAcordar1,
                                     controleObservacao=observacao, falaBem=falaBem,
                                     comunicacaoGestos=comunicaComGesto,
                                     gagueira=ehGago, enxergaBem=enxergaBem, destro=maoDireita,
                                     esquerda=maoEsquerda,
                                     fazBalbucio=fazBalbucio, anda=anda, seguraLapis=seguraLapis,
                                     sentaCorretamente=sentaCorretamente, caiMuito=caiMuito,
                                     cansaFacil=cansa,
                                     demonstraAfeto=demonstraAfeto, solicitaAfeto=solicitaAfeto,
                                     medroso=ehMedroso,
                                     agressivo=ehAgressivo, reageContrariado=reage, tique=possuiTique,
                                     choraFacilidade=choraFacil,
                                     sabeEspear=sabeEsperar, obedeceOrdens=obedeceOrdens,
                                     fazAmizade=fazAmizades,
                                     isolase=isolase, compartilha=sabeDividir, seRelaciona=seRelaciona,
                                     pronuciaCorretamente=pronuciaCorreto,
                                     expressaPensanetos=expressaPensamento,
                                     transmiteRecados=transmiteRecados, fazPedido=instrucoes,
                                     composicaoFamiliar=composicaoFamiliar,
                                     descricaoUsuario=descrisaoUsuario,
                                     data=dataTriagem, pessoaQuestionada=pessoaQuestionada, musica=musica, danca=danca,
                                     pintura=pintura, jiujitsu=jiujitsu, edFisica=edFisica, informatica=informatica,
                                     robotica=robotica, teatro=teatro)

    nomeTurma = request.POST['turmaTriagem']
    nomeTurma = nomeTurma.split('/')
    nomeTurma = nomeTurma[0][0:len(nomeTurma[0]) - 1]
    turma = Turma.objects.get(nome=nomeTurma)
    turma.ususario.add(usuarioT)

    PEI.objects.create(usuario=usuarioT, turma=turma)

    return HttpResponseRedirect(reverse('pedagogico:listar_triagemSocial'))


def editarTriagemM(request, id_triagem):
    triagem = TriagemPedagogica.objects.get(pk=id_triagem)

    triagem.alimentacao = request.POST['alimentacao']
    triagem.cuidador = request.POST['cuidador']
    triagem.responsavel = request.POST['responsavel']

    if request.POST['urinario'] == "sim":
        triagem.controleUrinario = True
    else:
        triagem.controleUrinario = False

    if request.POST['esfincter'] == "sim":
        triagem.controleEsfincter = True
    else:
        triagem.controleEsfincter = False

    if 'segunda' in request.POST:
        if request.POST['segunda'] == "segunda":
            triagem.segunda = True
        else:
            triagem.segunda = False
    else:
        triagem.segunda = False

    if 'terca' in request.POST:
        if request.POST['terca'] == "terca":
            triagem.terca = True
        else:
            triagem.terca = False
    else:
        triagem.terca = False

    if 'quarta' in request.POST:
        if request.POST['quarta'] == "quarta":
            triagem.quarta = True
        else:
            triagem.quarta = False
    else:
        triagem.quarta = False

    if 'quinta' in request.POST:
        if request.POST['quinta'] == "quinta":
            triagem.quinta = True
        else:
            triagem.quinta = False
    else:
        triagem.quinta = False

    if 'sexta' in request.POST:
        if request.POST['sexta'] == "sexta":
            triagem.sexta = True
        else:
            triagem.sexta = False
    else:
        triagem.sexta = False

    triagem.dormeCom = request.POST['dormeCom']
    horaDormir = request.POST['horaDormir']
    horaAcordar = request.POST['horaAcordar']

    triagem.horarioDormir = parse_time(horaDormir)
    triagem.horarioAcordar = parse_time(horaAcordar)

    triagem.composicaoFamiliar = request.POST['composicaoFamiliar']
    triagem.observacao = request.POST['observacao']

    # .............PEDAGOGICO...........

    triagem.musica = request.POST['musica']
    triagem.danca = request.POST['danca']
    triagem.pintura = request.POST['pintura']
    triagem.jiujitsu = request.POST['jiujtso']
    triagem.edFisica = request.POST['edFisica']
    triagem.informatica = request.POST['informatica']
    triagem.robotica = request.POST['robotica']
    triagem.teatro = request.POST['teatro']

    # .............ASPECTOS DE DESENVOLVIMENTO...........

    triagem.falaBem = request.POST['fala']
    triagem.comunicacaoGestos = request.POST['gestos']
    triagem.gagueira = request.POST['gago']
    triagem.enxergaBem = request.POST['enxerga']
    triagem.destro = request.POST['direita']
    triagem.esquerda = request.POST['esquerda']
    triagem.fazBalbucio = request.POST['balbucio']

    # .............ASPECTO FISICO MOTOR...........

    triagem.anda = request.POST['anda']
    triagem.seguraLapis = request.POST['segura']
    triagem.sentaCorretamente = request.POST['senta']
    triagem.caiMuito = request.POST['cai']
    triagem.cansaFacil = request.POST['cansa']

    # .............ASPECTO EMOCIONAL...........

    triagem.demonstraAfeto = request.POST['demonstra']
    triagem.solicitaAfeto = request.POST['solicita']
    triagem.medroso = request.POST['medroso']
    triagem.agressivo = request.POST['agressivo']
    triagem.reageContrariado = request.POST['reage']
    triagem.tique = request.POST['tique']
    triagem.choraFacilidade = request.POST['chora']

    # .............ASPECTO SOCIAL...........

    triagem.sabeEspear = request.POST['espera']
    triagem.obedeceOrdens = request.POST['obedece']
    triagem.fazAmizade = request.POST['amizades']
    triagem.isolase = request.POST['isola']
    triagem.compartilha = request.POST['divide']
    triagem.seRelaciona = request.POST['relaciona']

    # .............ASPECTO INTELECTUAL...........

    triagem.pronuciaCorretamente = request.POST['pronucia']
    triagem.expressaPensanetos = request.POST['expressa']
    triagem.transmiteRecados = request.POST['recado']
    triagem.fazPedido = request.POST['instrucoes']

    triagem.descricaoUsuario = request.POST['descricao']

    # nomeTurma = request.POST['turmaTriagem']
    # nomeTurma = nomeTurma.split('/')
    # nomeTurma = nomeTurma[0][0:len(nomeTurma[0]) - 1]
    # turma = Turma.objects.get(nome=nomeTurma)
    # turma.ususario.add(triagem.usuario)

    triagem.save()

    return HttpResponseRedirect(reverse('pedagogico:listagem_pedagogica'))


def desempenho(request):
    d = request.GET.get('d', None)
    id = request.GET.get('id', None)

    data = {'certo': False}
    try:
        frequencia = Frequencia.objects.get(pk=id)
        frequencia.desempenho = d
        frequencia.save()
        data['certo'] = True
        return JsonResponse(data)

    except Exception as e:
        return JsonResponse(data)


def falta(request):
    if request.GET.get('ckb', None) == "true":
        d = True
    else:
        d = False
    id = request.GET.get('id', None)

    data = {'certo': False}
    try:
        frequencia = Frequencia.objects.get(pk=id)
        frequencia.falta = d
        frequencia.save()
        data['certo'] = True
        return JsonResponse(data)

    except Exception as e:
        return JsonResponse(data)


def registrar_pei(request):
    pei = PEI.objects.get(pk=request.POST['pei'])
    # Comunicação Oral

    relataAcontecimentos = request.POST['relataAcontecimentos']
    lembraRecados = request.POST['lembraRecados']
    comunicacaoAlternativa = request.POST['comunicacaoAlternativa']
    linguagemOral = request.POST['linguagemOral']

    # Leitura e Escrita

    letrasNumeros = request.POST['letrasNumeros']
    reconheceDiferenca = request.POST['reconheceDiferenca']
    domina = request.POST['domina']
    ouve = request.POST['ouve']
    compreende = request.POST['compreende']
    participa = request.POST['participa']
    vocabulario = request.POST['vocabulario']
    soletrar = request.POST['soletrar']
    palavrasSimples = request.POST['palavrasSimples']
    assinar = request.POST['assinar']
    escreveEnd = request.POST['escreveEnd']
    ecrevePequnosTextos = request.POST['ecrevePequnosTextos']
    ditado = request.POST['ditado']
    leTextos = request.POST['leTextos']
    instrucoes = request.POST['instrucoes']
    habilidades = request.POST['habilidades']

    # Raciocínio Lógico-Matemático

    relacionaQuantidade = request.POST['relacionaQuantidade']
    problemasSimples = request.POST['problemasSimples']
    reconheceValores = request.POST['reconheceValores']
    identificaValor = request.POST['identificaValor']
    diferenciaNotasM = request.POST['diferenciaNotasM']
    agrupardinheiro = request.POST['agrupardinheiro']
    daTroco = request.POST['daTroco']
    possuiConceitos = request.POST['possuiConceitos']
    relacaoNumeroDia = request.POST['relacaoNumeroDia']
    identificaDia = request.POST['identificaDia']
    reconheceHoras = request.POST['reconheceHoras']
    horasDigital = request.POST['horasDigital']
    horasExatasPonteiros = request.POST['horasExatasPonteiros']
    horasExatasDigital = request.POST['horasExatasDigital']
    horasNaoExatasPonteiros = request.POST['horasNaoExatasPonteiros']
    horarioAcontecimentos = request.POST['horarioAcontecimentos']
    reconheceMedidas = request.POST['reconheceMedidas']
    conceitosMatematicos = request.POST['conceitosMatematicos']
    resolveOperacoes = request.POST['resolveOperacoes']
    demonstraCuriosidade = request.POST['demonstraCuriosidade']
    gostaJogas = request.POST['gostaJogas']
    organizaOrdemLogica = request.POST['organizaOrdemLogica']

    # Informática na Escola

    usaPcAutonomia = request.POST['usaPcAutonomia']
    sabeUsarPcNet = request.POST['sabeUsarPcNet']

    pei.relataAcontecimentos = relataAcontecimentos
    pei.lembraRecados = lembraRecados
    pei.comunicacaoAlternativa = comunicacaoAlternativa
    pei.linguagemOral = linguagemOral
    pei.letrasNumeros = letrasNumeros
    pei.reconheceDiferenca = reconheceDiferenca
    pei.domina = domina
    pei.ouve = ouve
    pei.compreende = compreende
    pei.participa = participa
    pei.vocabulario = vocabulario
    pei.soletrar = soletrar
    pei.palavrasSimples = palavrasSimples
    pei.assinar = assinar
    pei.escreveEnd = escreveEnd
    pei.ecrevePequnosTextos = ecrevePequnosTextos
    pei.ditado = ditado
    pei.leTextos = leTextos
    pei.instrucoes = instrucoes
    pei.habilidades = habilidades
    pei.relacionaQuantidade = relacionaQuantidade
    pei.problemasSimples = problemasSimples
    pei.reconheceValores = reconheceValores
    pei.identificaValor = identificaValor
    pei.diferenciaNotasM = diferenciaNotasM
    pei.agrupardinheiro = agrupardinheiro
    pei.daTroco = daTroco
    pei.possuiConceitos = possuiConceitos
    pei.relacaoNumeroDia = relacaoNumeroDia
    pei.identificaDia = identificaDia
    pei.reconheceHoras = reconheceHoras
    pei.horasDigital = horasDigital
    pei.horasExatasPonteiros = horasExatasPonteiros
    pei.horasExatasDigital = horasExatasDigital
    pei.horasNaoExatasPonteiros = horasNaoExatasPonteiros
    pei.horarioAcontecimentos = horarioAcontecimentos
    pei.reconheceMedidas = reconheceMedidas
    pei.conceitosMatematicos = conceitosMatematicos
    pei.resolveOperacoes = resolveOperacoes
    pei.demonstraCuriosidade = demonstraCuriosidade
    pei.gostaJogas = gostaJogas
    pei.organizaOrdemLogica = organizaOrdemLogica
    pei.usaPcAutonomia = usaPcAutonomia
    pei.sabeUsarPcNet = sabeUsarPcNet

    pei.save()

    return HttpResponseRedirect(reverse('pedagogico:lista_alunos', args=[pei.turma.id, ]))
