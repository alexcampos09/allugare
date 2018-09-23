from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "profilePic",
            "nome",
            "uf",
            "cidade",
            "universidade",
            "curso",
            "telefone",
            "bio",
        ]

    def profile(self, request, user):
        print('printing forms')
        user.uf = self.cleaned_data['uf']
        user.cidade = self.cleaned_data['cidade']
        user.telefone = self.cleaned_data['telefone']
        user.save()
