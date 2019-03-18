from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Turma)
admin.site.register(Aula)
admin.site.register(Frequencia)
admin.site.register(TriagemPedagogica)
admin.site.register(PEI)