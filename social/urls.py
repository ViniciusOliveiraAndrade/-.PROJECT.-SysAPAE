from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'social'
urlpatterns = [
    
    path('', views.index, name='index'),

    path('Perfil', views.perfil, name='perfil'),

        
    #Triagens
    path('Realizar_Triagem', views.triagem_realizar, name='triagem_realizar'),
    path('Cadastrar_Triagem', views.cadastrar_triagem, name='cadastrar_triagem'),
    path('Editar_Triagem/<int:triagem_id>', views.triagem_editar, name='triagem_editar'),
    path('Edit_Triagem', views.editar_triagem, name='editar_triagem'),
    path('Listar_Triagem', views.triagem_listar, name='triagem_listar'),
    path('Detalhe_Triagem/<int:triagem_id>', views.triagem_detalhe, name='triagem_detalhe'),

    #Usuario
    path('Listar_Usuarios/', views.usuarios_listar, name='usuarios_listar'),
    
    #visitas
    path('Agendar_Visita/<int:usuario_id>', views.visita_agendar, name='visita_agendar'),
    path('Listar_Visita', views.visita_listar, name='visita_listar'),
    path('Editar_Visita/<int:visita_id>', views.visita_editar, name='visita_editar'),

    #Eventos
    path('Cadastrar_Eventos', views.evento_cadastrar, name='evento_cadastrar'),

]