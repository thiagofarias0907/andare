from datetime import datetime

from django.contrib.messages.api import error
from accounts import models
from django.forms.models import inlineformset_factory
from career.models import Occupation, Skill
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.db.models import Q
from django.contrib import messages

from .models import OneOnOneMeeting, PdiPlan, PdiMeeting, ActionPlan, UserProfile, MeetingEvaluation
from .forms import ActionPlanStatusForm, MeetingEvaluationForm, OneOnOneMeetingForm, PdiMeetingForm, PdiPlanForm, ActionPlanForm, PdiPlanFormset, ActionPlanFormset, ActionPlanStatusFormset


def get_next_events(user):
    events = {}
    user   = UserProfile.objects.get(user=user)
    oneonone_meetings = OneOnOneMeeting.objects.filter(leader=user).filter(next_meeting_date__gt = datetime.now())
    pdi_meetings = PdiMeeting.objects.filter(Q(leader=user)| Q(follower=user)).filter(next_meeting__gt = datetime.today() )
    events['next_oneonone_meetings'] = oneonone_meetings
    events['next_pdi_meetings'] = pdi_meetings
    return events

@login_required(login_url='/accounts/login/')
def home(request):
    template = 'base.html'
    context = get_next_events(user=request.user)

    return render(request, template_name=template, context=context)


@login_required(login_url='/accounts/login/')
def one_on_one(request):
    template = 'core/one_on_one.html'
    context = get_next_events(user=request.user)
    leader   = UserProfile.objects.get(user=request.user)
    
    if (request.method == 'POST'):     
        form = OneOnOneMeetingForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.leader = leader
            f.save()
            return redirect('/events')
    leader = UserProfile.objects.get(user=request.user)
    form = OneOnOneMeetingForm(instance=leader)
    context['form'] = form
    return render(request, template_name=template, context=context)


@login_required(login_url='/accounts/login/')
def one_on_one_follower(request, follower):
    template = 'core/one_on_one.html'
    context = get_next_events(user=request.user)
    leader   = UserProfile.objects.get(user=request.user)
    follower_profile = UserProfile.objects.get(user__username= follower)

    if (request.method == 'POST'):     
        form = OneOnOneMeetingForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.leader = leader
            f.follower = follower_profile
            f.save()
            return redirect('/events')
    form = OneOnOneMeetingForm(instance=leader)
    context['follower'] = follower_profile
    context['form'] = form
    return render(request, template_name=template, context=context)


@login_required(login_url='/accounts/login/')
def update_one_on_one(request, leader_username, follower_username):
    template = 'core/one_on_one.html'
    context = get_next_events(user=request.user)
    leader   = UserProfile.objects.get(user__username=leader_username)
    follower = UserProfile.objects.get(user__username=follower_username)
    
    if (request.method == 'POST'):
        form = OneOnOneMeetingForm(request.POST, instance=[leader, follower])
        if form.is_valid():
            f = form.save(commit=False)
            f.leader = leader
            f.follower = follower
            f.save()
            return redirect('/events')
    form = OneOnOneMeetingForm(instance=[leader, follower])
    context['form'] = form
    return render(request, template_name=template, context=context)


@login_required(login_url='/accounts/login/')
def detail_one_on_one(request, id_meeting):
    template = 'core/detail_one_on_one.html'
    context = get_next_events(user=request.user)
    oneonone_meeting = OneOnOneMeeting.objects.get(id= id_meeting)
    context['meeting'] = oneonone_meeting
    return render(request, template_name=template, context=context)


@login_required(login_url='/accounts/login/')
def pdi_meeting(request, follower_username):
    template = 'core/pdi_meeting.html'
    context = get_next_events(user=request.user)
    follower = UserProfile.objects.get(user__username=follower_username)
    leader = UserProfile.objects.get(user=request.user)

    if (request.method == 'POST'):     
        pdi_form  = PdiMeetingForm(request.POST)
        plan_formset = PdiPlanFormset(request.POST, request.FILES, prefix='planformset')
        if plan_formset.is_valid() and pdi_form.is_valid():
            saved_pdi_meeting = pdi_form.save(commit=False)
            saved_pdi_meeting.follower = follower
            saved_pdi_meeting.leader = leader
            saved_pdi_meeting.save()
            # saved_plans = plan_formset.save(commit=False)
            for plan_form in plan_formset:
                if (plan_form.cleaned_data is None or len(plan_form.cleaned_data) == 0  ):
                    continue
                saved_plan = plan_form.save(commit=False)
                saved_plan.pdi_meeting = saved_pdi_meeting
                saved_plan.save()
                for nested in plan_form.nested:
                    if (nested.cleaned_data is None or len(nested.cleaned_data) == 0  ):
                        continue
                    nested.save(commit=False)
                    nested.pdi_plan = saved_plan
                    nested.save()
            return redirect('/events')
        else:
            messages.error(request, 'Falha ao salvar os dados')
    occupations = Occupation.objects.all()      
    # skills      = Skill.objects.all()
    form = PdiMeetingForm(instance=follower)
    context['form'] = form
    context['plan_formset'] = PdiPlanFormset(prefix='planformset')
    context['occupations'] = occupations
    context['skills'] = []
    context['follower'] = follower
    return render(request, template_name=template, context=context)


@login_required(login_url='/accounts/login/')
def edit_pdi_meeting(request, follower_username):
    template = 'core/pdi_meeting_update.html'
    context = get_next_events(user=request.user)
    follower = UserProfile.objects.get(user__username=follower_username)
    leader = UserProfile.objects.get(user=request.user)
    pdi_meeting = PdiMeeting.objects.filter(follower=follower).order_by('-date_time').first()
    pdi_plans = PdiPlan.objects.filter(pdi_meeting=pdi_meeting)
    form = PdiMeetingForm(instance=pdi_meeting)
    context['pdi_meeting'] = pdi_meeting
    pdi_plan_formset = PdiPlanFormset(instance=pdi_meeting, prefix='planformset')
    if (request.method == 'POST'):     
        pdi_form  = PdiMeetingForm(request.POST)
        plan_formset = PdiPlanFormset(request.POST, prefix='planformset')
        if plan_formset.is_valid() and pdi_form.is_valid():
            saved_pdi_meeting = pdi_form.save(commit=False)
            saved_pdi_meeting.follower = follower
            saved_pdi_meeting.leader = leader
            saved_pdi_meeting.id = pdi_meeting.id
            saved_pdi_meeting.save()
            for form in plan_formset:
                saved_plan = form.save(commit=False)
                saved_plan.id = form.cleaned_data['id'].id
                saved_plan.pdi_meeting = saved_pdi_meeting
                saved_plan.save()
                for nested in form.nested:
                    saved_nested = nested.save(commit=False)
                    saved_nested.pdi_plan = saved_plan
                    saved_nested.id = nested.cleaned_data['id'].id
                    saved_nested.save()
            return redirect('/events')
    occupations = Occupation.objects.all()      
    skills      = Skill.objects.all()
    context['form'] = form
    context['plan_formset'] = pdi_plan_formset
    context['occupations'] = occupations
    context['skills'] = skills
    context['follower'] = follower
    return render(request, template_name=template, context=context)



@login_required(login_url='/accounts/login/')
def detail_pdi_meeting(request, id_meeting):
    template = 'core/detail_pdi_meeting.html'
    context = get_next_events(user=request.user)
    pdi_meeting = PdiMeeting.objects.get(id=id_meeting)
    pdi_plans = PdiPlan.objects.filter(pdi_meeting=pdi_meeting)
    plans = []
    for plan in pdi_plans:
        plans.append((plan, ActionPlan.objects.filter(pdi_plan=plan)))
    
    context['pdi_meeting'] = pdi_meeting
    context['plans'] = plans
    return render(request, template_name=template, context=context)



@login_required(login_url='/accounts/login/')
def pdi_meeting_evaluate(request, follower_username):
    template = 'core/pdi_meeting_evaluate.html'
    context = get_next_events(user=request.user)
    follower = UserProfile.objects.get(user__username=follower_username)
    leader = UserProfile.objects.get(user=request.user)

    pdi_meeting = PdiMeeting.objects.filter(follower=follower).order_by('-date_time').first()
    pdi_plans = PdiPlan.objects.filter(pdi_meeting=pdi_meeting)
    actions_and_plans = []
    action_plans = {}
    action_plans['plan'] = None
    action_plans['actions'] = []
    for plan in pdi_plans:
        action_plans['plan'] = plan
        actions_plans_objects = ActionPlan.objects.filter(pdi_plan=plan)
        # action_plans['formset'] = ActionPlanFormset(prefix='actionplanformset'+str(plan.id),instance=plan)
        for action in actions_plans_objects:
            form = ActionPlanStatusForm(instance=action)
            action_plans['actions'].append({'action':action, 'form':form})
        action_plans['formset'] = ActionPlanStatusFormset(prefix='actionplanformset'+str(plan.id), instance=plan)
        actions_and_plans.append(action_plans)

    context['follower']     = follower
    context['pdi_meeting']  = pdi_meeting
    context['pdi_plans']    = pdi_plans
    context['actions_and_plans'] = actions_and_plans
    if (request.method == 'POST'):     
        for plan in pdi_plans:
            action_plan_form = ActionPlanStatusForm(request.POST, request.FILES)
            if action_plan_form.is_valid():
                saved_form = action_plan_form.save(commit=False)
                saved_form.pdi_plan_id = plan.id
                saved_form.save()
        return redirect('core:team')
    return render(request, template_name=template, context=context)


@login_required(login_url='/accounts/login/')
def list_events(request):
    context = get_next_events(user=request.user)
    user    = UserProfile.objects.get(user=request.user)

    if user.profile == 1:
        template = 'core/follower_events.html'
        oneonone_meetings = OneOnOneMeeting.objects.filter(follower=user)
        pdi_meetings = PdiMeeting.objects.filter(follower=user)
        evaluations = MeetingEvaluation.objects.filter(user_profile= user)
        evaluated = []
        for evaluation in evaluations:
            if evaluation.pdi_meeting is None:
                evaluated.append(evaluation.one_on_one)
            else:
                evaluated.append(evaluation.pdi_meeting)
        context['evaluations'] = evaluated
        context['one_on_ones'] = oneonone_meetings
        context['pdi_meetings'] = pdi_meetings
        return render(request, template_name=template, context=context)

    template = 'core/events.html'
    oneonone_meetings = OneOnOneMeeting.objects.filter(leader=user).order_by('-date_time')
    pdi_meetings = PdiMeeting.objects.filter(leader=user).order_by('-date_time')
    followers = []
    followers_objects = []
    for meeting in oneonone_meetings:
        profile = UserProfile.objects.get(id= meeting.follower_id)
        if profile not in followers:
            followers.append(profile)
    
    for meeting in pdi_meetings:
        profile = UserProfile.objects.get(id= meeting.follower_id)
        if profile not in followers:
            followers.append(profile)
    
    for follower in followers:
        pdis = PdiMeeting.objects.filter(leader=user).filter(follower=follower).order_by('-date_time')[:2]
        ones = OneOnOneMeeting.objects.filter(leader=user).filter(follower=follower).order_by('-date_time')[:2]
        followers_objects.append({'follower':follower, 'pdi_meetings':pdis, 'one_on_ones':ones})

    all_followers = UserProfile.objects.filter(creator=user)
    for follower in all_followers:
        if follower not in followers:
            followers_objects.append({'follower':follower, 'pdi_meetings':None, 'one_on_ones':None})

    context['one_on_ones'] = oneonone_meetings
    context['pdi_meetings'] = pdi_meetings
    context['followers'] = followers_objects
    return render(request, template_name=template, context=context)




@login_required(login_url='/accounts/login/')
def show_team(request):
    template = 'core/team.html'
    context = get_next_events(user=request.user)
    user = UserProfile.objects.get(user=request.user)
    all_pdi_meetings = PdiMeeting.objects.filter(leader=user).order_by('-date_time')
    followers_created = UserProfile.objects.filter(creator=user).exclude(user=request.user)
    followers = []
    pdi_meetings = []
    for meeting in all_pdi_meetings:
        profile = UserProfile.objects.get(id= meeting.follower_id)
        if profile not in followers:
            followers.append(profile)
            pdi_plans = PdiPlan.objects.filter(pdi_meeting=meeting)
            plans = []
            for plan in pdi_plans:
                plans.append({'plan':plan,'description':plan.description, 'plan_type':plan.plan_type})
            follower_pdi = {'follower':profile,'pdi_plans':plans}
            pdi_meetings.append(follower_pdi)
    
    new_followers = []
    for follower in followers_created:
        if follower not in followers:
            followers.append(follower)
            new_followers.append(follower)

    context['pdi_meetings'] = pdi_meetings
    context['followers']    = followers
    context['new_followers']= new_followers
    return render(request, template_name=template, context=context)




@login_required(login_url='/accounts/login/')
def meeting_evaluation(request, meeting_id, meeting_type):
    pdi_meeting = None
    one_on_one = None
    template = 'core/meeting_evaluation.html'
    context = get_next_events(user=request.user)
    profile = UserProfile.objects.get(user=request.user)
    if meeting_type == 'one_on_one':
        one_on_one = OneOnOneMeeting.objects.get(id=meeting_id)
    else:
        pdi_meeting = PdiMeeting.objects.get(id=meeting_id)

    if (request.method == 'POST'):     
        form = MeetingEvaluationForm(request.POST, request.FILES)
        if form.is_valid():
            saved_form = form.save(commit=False)
            saved_form.user_profile = profile
            saved_form.pdi_meeting  = pdi_meeting
            saved_form.one_on_one   = one_on_one
            saved_form.date_time    = datetime.now()
            saved_form.save()
        return redirect('core:events')

    form = MeetingEvaluationForm()
    context['form']  = form
    context['emojis'] = [(1,128557),(2,128552),(3,128560),(4,128551),(5,128543),(6,128542),(7,128533),(8,128524),(9,128521),(10,128540),(11,128578),(12,128522),(13,128526),(14,128513),(15,129321)]
    context['pdi_meeting']  = pdi_meeting
    context['one_on_one']   = one_on_one
    context['score_loop']   = range(1,11)
    return render(request, template_name=template, context=context)


@login_required(login_url='/accounts/login/')
def load_skills(request):
    template = 'core/skills_dropdown_list_options.html'
    context = {}    
    id_occupation = request.GET.get('id_occupation')
    skills = []
    if (id_occupation is not None) and (id_occupation != ''):
        skills = Skill.objects.filter(occupation_id=id_occupation).order_by('id')
    context['skills'] = skills
    return render(request, template_name=template,context=context)