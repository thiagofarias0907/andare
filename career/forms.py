from django import forms
from django.forms import fields, models

from .models import Skill, Occupation

class SkillForm(forms.ModelForm):  
    class Meta:
        model = Skill
        verbose_name = 'Formulário de Habilidades / Níveis'
        exclude = ['occupation']

class OccupationForm(forms.ModelForm):
    class Meta:
        model = Occupation
        verbose_name = 'Formulário de Cargos'
        exclude = ()

SkillFormset = forms.inlineformset_factory(Occupation, Skill, exclude=(), extra=3, min_num=1, max_num=4, can_delete=True)