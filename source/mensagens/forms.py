from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["anuncio", "mensagem"]

class ContactForm(forms.Form):
    email       = forms.EmailField(required=True)
    nome        = forms.CharField(required=True)
    mensagem    = forms.CharField(required=True, widget=forms.Textarea)
