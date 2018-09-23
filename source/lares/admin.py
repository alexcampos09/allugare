from django.contrib import admin
from django import forms

from .models import Imovel, ImovelPhotos
from .forms import ImovelForm

class ImovelOrderForm(forms.ModelForm):
    model = Imovel
    class Media:
        js = (
            '/static/js/jquery-latest.js',
            '/static/js/ui.base.js',
            '/static/js/ui.sortable.js',
            '/static/js/menu-sort.js',
        )

class ImovelPhotosInline(admin.TabularInline):
# class ImovelPhotosInline(admin.StackedInline):
    model = ImovelPhotos

class ImoveisAdmin(admin.ModelAdmin):
    extra = 3
    inlines = [ImovelPhotosInline]

    list_display = [
        "id",
        "referencia",
        "__str__",
        "user",
        "active",
        "tipo_imovel",
        "qtd_quartos",
        "preco_total",
        "timestamp",
        "updates",
    ]
    readonly_fields = ['updates', 'timestamp',]
    # prepopulated_fields = {}
    form = ImovelForm
    class Meta:
        model = Imovel


admin.site.register(Imovel,
    # inlines = [ImovelPhotosInline],
    # form = ImovelOrderForm,
    ImoveisAdmin
    )
