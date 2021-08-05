from django.forms.models import inlineformset_factory
from career.models import Occupation, Skill
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.apps import apps

from .models import PdiPlan, PdiMeeting, ActionPlan, UserProfile
from .forms import OneOnOneMeetingForm, PdiMeetingForm, PdiPlanForm, ActionPlanForm

@login_required(login_url='/accounts/login/')
def home(request):
    template = 'base.html'
    context = {}
    return render(request, template_name=template, context=context)

def one_on_one(request):
    template = 'core/one_on_one.html'
    context = {}
    leader   = UserProfile.objects.get(user=request.user)
    if (request.method == 'POST'):     
        form = OneOnOneMeetingForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.leader = leader
            f.save()
            return redirect('/')
    leader = UserProfile.objects.get(user=request.user)
    form = OneOnOneMeetingForm(instance=leader)
    context['form'] = form
    return render(request, template_name=template, context=context)

def update_one_on_one(request, leader_username, follower_username):
    template = 'core/one_on_one.html'
    context = {}
    leader   = UserProfile.objects.get(user__username=leader_username)
    follower = UserProfile.objects.get(user__username=follower_username)
    if (request.method == 'POST'):
        form = OneOnOneMeetingForm(request.POST, instance=[leader, follower])
        if form.is_valid():
            f = form.save(commit=False)
            f.leader = leader
            f.follower = follower
            f.save()
            return redirect('/')
    form = OneOnOneMeetingForm(instance=[leader, follower])
    context['form'] = form
    return render(request, template_name=template, context=context)



def pdi_meeting(request, follower_username):
    template = 'core/pdi_meeting.html'
    context = {}
    follower = UserProfile.objects.get(user__username=follower_username)
    leader = UserProfile.objects.get(user=request.user)
    pdi_plan_formset = inlineformset_factory(PdiMeeting, PdiPlan, exclude=(), can_delete=False, extra=0, min_num=1, max_num=5)
    pdi_action_formset = inlineformset_factory(PdiPlan, ActionPlan, exclude=(), can_delete=False, extra=0, min_num=1, max_num=5)
    if (request.method == 'POST'):     
        pdi_form  = PdiMeetingForm(request.POST)
        plan_formset = pdi_plan_formset(request.POST, request.FILES, prefix='planformset')
        action_formset = pdi_action_formset(request.POST, request.FILES, prefix='actionformset')
        if plan_formset.is_valid() and action_formset.is_valid() and pdi_form.is_valid():
            saved_pdi_meeting = pdi_form.save(commit=False)
            saved_pdi_meeting.follower = follower
            saved_pdi_meeting.leader = follower
            saved_pdi_meeting.save()

            plan_formset_to_commit = plan_formset.save(commit=False)
            counter = 0
            for form in plan_formset_to_commit:
                form.pdi_meeting = PdiMeeting.objects.get(id=saved_pdi_meeting.id)
                form.save()
                action_formset_to_commit = action_formset.save(commit=False)
                for action_form in action_formset_to_commit:
                    action_form.pdi_plan = PdiPlan.objects.get(id=form.id)
                    action_form.save()
                
            return redirect('/')
    occupations = Occupation.objects.get()      
    skills      = Skill.objects.get()
    form = PdiMeetingForm(instance=follower)
    context['form'] = form
    context['plan_formset'] = pdi_plan_formset(prefix='planformset')
    context['action_formset'] = pdi_action_formset(prefix='actionformset')
    context['occupations'] = occupations
    context['skills'] = skills
    context['follower'] = follower
    return render(request, template_name=template, context=context)

    
    # template = 'project_management/create_methodologysteps.html'
    # context = {}
    # methodology_steps_formSet = inlineformset_factory(MethodologySteps, Steps, exclude=(), can_delete=False,  min_num= 3, max_num= 10)
    # if request.method == "POST":
    #     methodology_form = MethodologyStepsForm(request.POST)
    #     formset = methodology_steps_formSet(request.POST, request.FILES,prefix='stepsformset')
    #     if formset.is_valid() and methodology_form.is_valid():
    #         methodology_form.save()
    #         formset_save = formset.save(commit=False)
    #         for form in formset_save:
    #             form.methodology = MethodologySteps.objects.get(name=methodology_form.data.get('name'))
    #             form.save()
    #         messages.success(request,'Metodologia adicionada com sucesso!')
    #     else:
    #         messages.warning(request,'Erro ao salvar! Verifique os dados inseridos')
    # else:
    #     methodology_form = MethodologyStepsForm()
    #     formset = methodology_steps_formSet(prefix='stepsformset')
    # context['steps_formset'] = formset
    # context['methodology_form'] = methodology_form
    # return render(request, template_name=template, context=context)


# carrer_goal = models.
# carrer_tier_goal = mo
# interest_one = models
# interest_two = models
# interest_three = mode
# interest_four = model
# interest_five = model
# plan_description = mo
# plan_type = models.Sm
# plan_action = models.
# plan_action_due_date 
# plan_action_status = 