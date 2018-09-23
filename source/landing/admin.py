from django.contrib import admin
from .forms import LandingPageForm
from .models import LandingPage

class LandingPageAdmin(admin.ModelAdmin):
    list_display = ["nome_completo", "__str__", "telefone", "caracteristicas", "timestamp",]
    form = LandingPageForm
    class Meta:
        model = LandingPage

admin.site.register(LandingPage, LandingPageAdmin)
