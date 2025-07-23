from django import forms
from .models import Autobot

class AutobotForm(forms.ModelForm):
    class Meta:
        model = Autobot
        fields = ['nome', 'tipo', 'poder', 'frase_batalha']