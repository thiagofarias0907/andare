from core.models import ActionPlan, OneOnOneMeeting, PdiMeeting, PdiPlan
from django import forms

class OneOnOneMeetingForm(forms.ModelForm):
    class Meta:
        model = OneOnOneMeeting
        verbose_name = 'Formulário reunião 1:1'
        exclude = ['leader']


class PdiMeetingForm(forms.ModelForm):
    class Meta:
        model = PdiMeeting
        verbose_name = 'Formulário reunião PDI'
        exclude = ['leader','follower']

class PdiPlanForm(forms.ModelForm):
    class Meta:
        model = PdiPlan
        verbose_name = 'Formulário Plano'
        exclude = []

class ActionPlanForm(forms.ModelForm):
    class Meta:
        model = ActionPlan
        verbose_name = 'Formulário Plano de Ação'
        exclude = []
