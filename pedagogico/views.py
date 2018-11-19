from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
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
    # usuarioTurma = UsuarioTurma.objects.all()
    return render(request, 'pedagogico/cadastrar_aula.html', {"turma": id_turma})


@login_required
def frequencia(request, id_aula):
    # usuarios = Usuario.objects.all()

    aula = Aula.objects.get(pk=id_aula)
    turma = aula.turma_set.all()[0]

    # aulas = Aula.objects.all()

    # triagens = Triagem.objects.all()

    return render(request, 'pedagogico/frequencia.html', {"usuarios": turma.ususario.all(), "aula": aula})


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

    pedagogica_t = TriagemPedagogica.objects.all()

    return render(request, 'pedagogico/listar_triagemSocial.html',
                  {"triagemSocial": triagemSocial, "triagemPedagogica": pedagogica_t})


@login_required
def listar_turmas(request):
    listaTurmas = Turma.objects.all()
    return render(request, 'pedagogico/listar_turmasCordenacao.html', {"listaTurmas": listaTurmas})


@login_required
def listar_aulas(request, id_turma):
    aulas = Turma.objects.get(pk=id_turma).aula.all()
    return render(request, 'pedagogico/listar_aulas.html', {"aulas": aulas, 'id_turma': id_turma})


@login_required
def listas_turmasProf(request):
    turmas = Turma.objects.all()

    return render(request, "pedagogico/listar_turmasProf.html", {"turmas": turmas})


@login_required
def detalhes_aula(request, id_aula):
    id = Aula.objects.get(pk=id_aula)

    return render(request, "pedagogico/aula_detalhes.html", {"idAula": id})


@login_required
def lista_Tpedagogica(request):
    pedagogica_t = TriagemPedagogica.objects.all()

    return render(request, 'pedagogico/listagem_pedagogica.html', {"listaPedagogica": pedagogica_t})


@login_required
def ver_turmaCoord(request, id_turma):
    turma = Turma.objects.get(pk=id_turma)

    listaAlunos = turma.ususario.all()

    return render(request, 'pedagogico/ver_turmaCoordenacao.html', {"listaAlunos": listaAlunos, "Turma":turma})

@login_required
def editar_triagem(request, idTriagem):
    # id = TriagemPedagogica.objects.get(pk=idTriagem)

    return render(request, 'pedagogico/editar_triagem.html', {"idTriagem": idTriagem})


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

    frequencia = Frequencia.objects.create()
    aula = Aula.objects.create(data=dataAula, situacao=situacao, conteudo=request.POST["conteudo"],
                               titulo=request.POST["tituloAula"], frequencia=frequencia)
    turma = Turma.objects.get(pk=request.POST['id_turma'])
    turma.aula.add(aula)
    turma.save()

    return HttpResponseRedirect(reverse('pedagogico:listar_aulas', args=(turma.id,)))


def editar_aulas(request, id_aula):
    aula = get_object_or_404(Aula, pk=id_aula)
    if "tituloAula" in request.POST:
        aula = get_object_or_404(Aula, pk=id_aula)

        data = request.POST['dataAula']
        data = data.split('-')

        dataAula = datetime.datetime(int(data[0]), int(data[1]), int(data[2]))

        if request.POST["situacao"] == "aberto":
            situacao = True
        else:
            situacao = False

        aula.data = dataAula
        aula.situacao = situacao
        aula.conteudo = request.POST["conteudo"]
        aula.titulo = request.POST["tituloAula"]
        aula.avaliacaoAula = request.POST['avaliacao']
        aula.save()

        turma = aula.turma_set.all()[0:1]
        turma = turma[0]

        return HttpResponseRedirect(reverse('pedagogico:listar_aulas', args=(turma.id,)))
    return render(request, "pedagogico/editar_aula.html", {"aula": aula})


def editar_turma(request, id_turma):
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

    if request.POST['turno'] == "manha":
        turno = True
    else:
        turno = False

    usuarioT = Usuario.objects.get(pk=request.POST['usuario'])
    # municipio = request.POST['municipio']
    # pai = request.POST['pai']
    # mae = request.POST['mae']

    alimentacao = request.POST['alimentacao']
    cuidador = request.POST['cuidador']
    responsavel = request.POST['responsavel']

    if request.POST['checkboxsize'] == "segunda":
        segunda = True
    else:
        segunda = False

    if request.POST['checkboxsize'] == "terca":
        terca = True
    else:
        terca = False

    if request.POST['checkboxsize'] == "quarta":
        quarta = True
    else:
        quarta = False

    if request.POST['checkboxsize'] == "quinta":
        quinta = True
    else:
        quinta = False

    if request.POST['checkboxsize'] == "sexta":
        sexta = True
    else:
        sexta = False

    dormeCom = request.POST['dormeCom']
    horaDormir = request.POST['horaDormir']
    horaAcordar = request.POST['horaAcordar']

    horaDormir1 = parse_time(horaDormir)
    horaAcordar1 = parse_time(horaAcordar)

    composicaoFamiliar = request.POST['composicaoFamiliar']
    observacao = request.POST['observacao']

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
                                     controleEsfincter=esfincter, turno=turno,
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
                                     data=dataTriagem, pessoaQuestionada=pessoaQuestionada)

    turma = Turma.objects.get(nome=request.POST['turmaTriagem'])
    turma.ususario.add(usuarioT)

    return HttpResponseRedirect(reverse('pedagogico:index'))


def editarTriagem(request, id_triagem):
    triagem = get_object_or_404(TriagemPedagogica, pk=id_triagem)
