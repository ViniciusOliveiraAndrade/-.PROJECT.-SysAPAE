from django.urls import path

from . import views

app_name = "pedagogico"

urlpatterns = [
    path('', views.index, name="index"),
    path('criar_turma', views.criar_turma, name="criar_turma"),
    path('cadastrar_turmas', views.cadastrar_turmas, name="cadastrar_turmas"),
    path('cadastrar_aula', views.cadastrar_aula, name='cadastrar_aula'),
    path('criar_aula', views.cadastrar_aulas, name='cadastrar_aulas'),
    path('frequencia', views.frequencia, name='frequencia'),
    path('triagem_pedagogica', views.triagem_pedagogica, name='triagem_pedagogica'),
]

