from django.contrib import admin

from .models import *
# from core.models import *

admin.site.register(CID)
admin.site.register(Usuario)
admin.site.register(Cargo)
admin.site.register(Funcionario)
admin.site.register(Triagem)
admin.site.register(Visita)
admin.site.register(Evento)
admin.site.register(Lista)