from django import forms
from .models import EventoPartido, ComentarioPartido

class EventoPartidoForm(forms.ModelForm):
    class Meta:
        model = EventoPartido
        fields = ['tipo', 'minuto', 'jugador', 'comentario']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'minuto': forms.NumberInput(attrs={'class': 'form-control'}),
            'jugador': forms.Select(attrs={'class': 'form-control'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ComentarioPartidoForm(forms.ModelForm):
    class Meta:
        model = ComentarioPartido
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }