from django.urls import path

from . import views

app_name = "pedagogico"

urlpatterns = [
    #HOME
    path('', views.index, name="index"),

    #TURMAS
    path('criar_turma', views.criar_turma, name="criar_turma"),
    path('cadastrar_turmas', views.cadastrar_turmas, name="cadastrar_turmas"),
    path('listar_turmas', views.listar_turmas, name="listar_turmas"),
    path('editar_turma/<int:id_turma>', views.editar_turma, name="editar_turma"),
    path('deletar_turma/<int:id_turma>', views.deletar_turma, name="deletar_turma"),
    path('turma_prof', views.listas_turmasProf, name="minhas_turmas"),

    #AULAS
    path('criar_aula', views.cadastrar_aulas, name='cadastrar_aulas'),
    path('cadastrar_aula/<int:id_turma>', views.cadastrar_aula, name='cadastrar_aula'),
    path('listar_aulas/<int:id_turma>', views.listar_aulas, name='listar_aulas'),
    path('editar_aula/<int:id_aula>', views.editar_aulas, name='editar_aula'),
    path('deletar_aula/<int:id_aula>', views.deletar_aula, name="deletar_aula"),

    #FREQUENCIA
    path('frequencia/<int:id_aula>', views.frequencia, name='frequencia'),

    #TRIAGEM
    path('listar_triagemSocial', views.listar_triagemSocial, name='listar_triagemSocial'),
    path('triagem_pedagogica/<int:id_usuario>', views.triagem_pedagogica, name='triagem_pedagogica'),
]

