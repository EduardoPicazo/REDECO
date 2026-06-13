from django import forms
from .models import Queja, Producto, Causa

class QuejaForm(forms.ModelForm):
    class Meta:
        model = Queja
        fields = ['fecha_consulta', 'estado', 'fecha_cierre', 'producto', 'causa', 'medio']
        widgets = {
            'fecha_consulta': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'form-select', 'id': 'id_estado'}),
            'fecha_cierre': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_fecha_cierre'}),
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'causa': forms.Select(attrs={'class': 'form-select'}),
            'medio': forms.TextInput(attrs={'class': 'form-control'}),
        }
