from django import forms
from .models import LandingPage

class LandingPageForm(forms.ModelForm):
    class Meta:
        model = LandingPage
        fields = [
            "nome_completo",
            "email",
            "telefone",
            "caracteristicas",
            ]

        widgets = {
          'caracteristicas': forms.Textarea(attrs={'rows':3, 'cols':15, 'placeholder':'Exemplo: procuro um apt de 2 quartos próximo da UFSCar. Tenho um carro e um cachorro.'}),

        }
