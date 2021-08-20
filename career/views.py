from career.models import Occupation, Skill
from career.forms import OccupationForm, SkillFormset
from django.http import request
from django.shortcuts import redirect, render, get_object_or_404

from core.views import get_next_events

# Create your views here.

def add_occupation(request):
    template = 'career/occupation.html'
    context = get_next_events(user=request.user)
    if (request.method == 'POST'):
        occupation_form = OccupationForm(request.POST)
        skill_formset = SkillFormset(request.POST, request.FILES, prefix='skillformset')
        if occupation_form.is_valid() and skill_formset.is_valid():
            saved_occupation = occupation_form.save(commit=False)
            saved_occupation.save()
            for form in skill_formset:
                if (form.cleaned_data is None or len(form.cleaned_data) == 0  ):
                    continue
                saved_skill = form.save(commit=False)
                saved_skill.occupation = saved_occupation
                saved_skill.save()
        return redirect('career:list_career')    
    
    form = OccupationForm()
    formset = SkillFormset(prefix='skillformset')
    context['form'] = form
    context['formset'] = formset
    return render(request, template_name=template, context=context)

def edit_occupation(request, occupation_id):
    template = 'career/occupation.html'
    context = get_next_events(user=request.user)
    occupation = Occupation.objects.get(id=occupation_id)
    skills = Skill.objects.filter(occupation= occupation)
    skill_formset = SkillFormset(prefix='skillformset', instance=occupation)
    if (request.method == 'POST'):
        Occupation
        skillFormset = SkillFormset(request.POST, prefix='skillformset')
        return redirect('career:list_career')    
    
    form = OccupationForm(instance=occupation)
    context['form'] = form
    context['formset'] = skill_formset
    context['occupation'] = occupation
    context['skills'] = skills
    return render(request, template_name=template, context=context)



def list_all(request):
    template = 'career/career_list.html'
    context = get_next_events(user=request.user)
    occupations = Occupation.objects.all()
    occupations_and_skills = []
    for occupation in occupations:
        skills = Skill.objects.filter(occupation= occupation)
        occupations_and_skills.append({'occupation':occupation,'skills':skills})
    context['occupations_and_skills'] = occupations_and_skills
    return render(request, template_name=template, context=context)




def delete_occupation(request, occupation_id):
    occupation = get_object_or_404(Occupation, id=occupation_id)
    occupation.delete()
    return redirect("career:list_career")