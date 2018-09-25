from django.contrib import admin

from .models import Usuario, Funcionario, Triagem, Visita

admin.site.register(Usuario)
admin.site.register(Funcionario)
admin.site.register(Triagem)
admin.site.register(Visita)