from django.urls import path

from . import views

app_name = 'social'
urlpatterns = [
    path('', views.index, name='index'),
    
    path('Realizar_Triagem', views.triagem_realizar, name='triagem_realizar'),
    path('Cadastrar_Triagem', views.cadastrar_triagem, name='cadastrar_triagem'),

    path('Bucar_Triagem', views.triagem_buscar, name='triagem_buscar'),
    path('Editar_Triagem/<int:triagem_id>', views.triagem_editar, name='triagem_editar'),
    path('Edit_Triagem', views.editar_triagem, name='editar_triagem'),
    
    path('Listar_Triagem', views.triagem_listar, name='triagem_listar'),
    
    path('Agendar_Visita', views.visita_agendar, name='visita_agendar'),

    path('Listar_Visita', views.visita_listar, name='visita_listar'),

]