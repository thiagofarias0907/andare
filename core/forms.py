from django.forms import widgets
from core.models import ActionPlan, MeetingEvaluation, OneOnOneMeeting, PdiMeeting, PdiPlan
from django import forms

class OneOnOneMeetingForm(forms.ModelForm):
    class Meta:
        model = OneOnOneMeeting
        verbose_name = 'Formulário reunião 1:1'
        exclude = ['leader','follower']
        widgets = {'next_meeting_date': widgets.DateInput({'type':'date'})}


class PdiMeetingForm(forms.ModelForm):
    class Meta:
        model = PdiMeeting
        verbose_name = 'Formulário reunião PDI'
        exclude = ['leader','follower','next_meeting']

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

class ActionPlanStatusForm(forms.ModelForm):
    class Meta:
        model = ActionPlan
        verbose_name = 'Formulário Plano de Ação'
        fields = ['id','status']

        
ActionPlanStatusFormset = forms.inlineformset_factory(PdiPlan, ActionPlan,fields = ['status'], can_delete=False, extra=0, 
        widgets = {'due_date': widgets.DateInput({'type':'date'})}
)

# NESTED form for the PDI and its plan actions
ActionPlanFormset = forms.inlineformset_factory(PdiPlan, ActionPlan, exclude=(), can_delete=True, extra=0, min_num=3, max_num=5,
        widgets = {'due_date': widgets.DateInput({'type':'date'})}
)
class BasePdiPlanFormset(forms.BaseInlineFormSet):
    
    def add_fields(self, form, index) -> None:
        super(BasePdiPlanFormset, self).add_fields(form, index)

        form.nested = ActionPlanFormset(
            instance=form.instance, 
            data=form.data if form.is_bound else None, 
            files=form.files if form.is_bound else None, 
            prefix='actionplan-%s' % (form.prefix)
            )

    def is_valid(self):
        result = super(BasePdiPlanFormset, self).is_valid()
        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()
        return result
    
    def save(self, commit=True):

        result = super(BasePdiPlanFormset, self).save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)
        return result

PdiPlanFormset = forms.inlineformset_factory(PdiMeeting, PdiPlan, formset=BasePdiPlanFormset, exclude=(), can_delete=True, extra=0, min_num=1, max_num=5)


class MeetingEvaluationForm(forms.ModelForm):
    class Meta:
        model = MeetingEvaluation
        verbose_name = 'Formulário Avaliação Reunião'
        exclude = ['one_on_one','pdi_meeting','user_profile','date_time']
        widgets = {
          'commentary': forms.Textarea(attrs={'rows':3, 'cols':200}),
        }

