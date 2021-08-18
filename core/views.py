from datetime import datetime
from accounts import models
from django.forms.models import inlineformset_factory
from career.models import Occupation, Skill
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.apps import apps

from .models import OneOnOneMeeting, PdiPlan, PdiMeeting, ActionPlan, UserProfile
from .forms import ActionPlanStatusForm, MeetingEvaluationForm, OneOnOneMeetingForm, PdiMeetingForm, PdiPlanForm, ActionPlanForm, PdiPlanFormset, ActionPlanFormset, ActionPlanStatusFormset

@login_required(login_url='/accounts/login/')
def home(request):
    template = 'base.html'
    context = {}
    leader   = UserProfile.objects.get(user=request.user)
    oneonone_meetings = OneOnOneMeeting.objects.filter(leader=leader)
    pdi_meetings = PdiMeeting.objects.filter(leader=leader)
    context['one_on_ones'] = oneonone_meetings
    context['pdi_meetings'] = pdi_meetings
    return render(request, template_name=template, context=context)

def one_on_one(request):
    template = 'core/one_on_one.html'
    context = {}
    leader   = UserProfile.objects.get(user=request.user)
    oneonone_meetings = OneOnOneMeeting.objects.filter(leader=leader)
    pdi_meetings = PdiMeeting.objects.filter(leader=leader)
    context['one_on_ones'] = oneonone_meetings
    context['pdi_meetings'] = pdi_meetings
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

def one_on_one_follower(request, follower):
    template = 'core/one_on_one.html'
    context = {}
    leader   = UserProfile.objects.get(user=request.user)
    oneonone_meetings = OneOnOneMeeting.objects.filter(leader=leader)
    pdi_meetings = PdiMeeting.objects.filter(leader=leader)
    context['one_on_ones'] = oneonone_meetings
    context['pdi_meetings'] = pdi_meetings
    if (request.method == 'POST'):     
        form = OneOnOneMeetingForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.leader = leader
            f.save()
            return redirect('/events')
    follower_profile = UserProfile.objects.get(user__username= follower)
    form = OneOnOneMeetingForm(instance=leader)
    context['follower'] = follower_profile
    context['form'] = form
    return render(request, template_name=template, context=context)

def update_one_on_one(request, leader_username, follower_username):
    template = 'core/one_on_one.html'
    context = {}
    leader   = UserProfile.objects.get(user__username=leader_username)
    follower = UserProfile.objects.get(user__username=follower_username)
    oneonone_meetings = OneOnOneMeeting.objects.filter(leader=leader)
    pdi_meetings = PdiMeeting.objects.filter(leader=leader)
    context['one_on_ones'] = oneonone_meetings
    context['pdi_meetings'] = pdi_meetings
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



# def pdi_meeting(request, follower_username):
#     template = 'core/pdi_meeting.html'
#     context = {}
#     follower = UserProfile.objects.get(user__username=follower_username)
#     leader = UserProfile.objects.get(user=request.user)
#     oneonone_meetings = OneOnOneMeeting.objects.filter(leader=leader)
#     pdi_meetings = PdiMeeting.objects.filter(leader=leader)
#     context['one_on_ones'] = oneonone_meetings
#     context['pdi_meetings'] = pdi_meetings
#     pdi_plan_formset = inlineformset_factory(PdiMeeting, PdiPlan, exclude=(), can_delete=False, extra=0, min_num=1, max_num=5)
#     pdi_action_formset = inlineformset_factory(PdiPlan, ActionPlan, exclude=(), can_delete=False, extra=0, min_num=1, max_num=5)
#     if (request.method == 'POST'):     
#         pdi_form  = PdiMeetingForm(request.POST)
#         plan_formset = pdi_plan_formset(request.POST, request.FILES, prefix='planformset')
#         action_formset = pdi_action_formset(request.POST, request.FILES, prefix='actionformset')
#         if plan_formset.is_valid() and action_formset.is_valid() and pdi_form.is_valid():
#             saved_pdi_meeting = pdi_form.save(commit=False)
#             saved_pdi_meeting.follower = follower
#             saved_pdi_meeting.leader = follower
#             saved_pdi_meeting.save()

#             plan_formset_to_commit = plan_formset.save(commit=False)
#             counter = 0
#             for form in plan_formset_to_commit:
#                 form.pdi_meeting = PdiMeeting.objects.get(id=saved_pdi_meeting.id)
#                 form.save()
#                 action_formset_to_commit = action_formset.save(commit=False)
#                 for action_form in action_formset_to_commit:
#                     action_form.pdi_plan = PdiPlan.objects.get(id=form.id)
#                     action_form.save()
                
#             return redirect('/')
#     occupations = Occupation.objects.all()      
#     skills      = Skill.objects.all()
#     form = PdiMeetingForm(instance=follower)
#     context['form'] = form
#     context['plan_formset'] = pdi_plan_formset(prefix='planformset')
#     context['action_formset'] = pdi_action_formset(prefix='actionformset')
#     context['occupations'] = occupations
#     context['skills'] = skills
#     context['follower'] = follower
#     return render(request, template_name=template, context=context)



def pdi_meeting(request, follower_username):
    template = 'core/pdi_meeting.html'
    context = {}
    follower = UserProfile.objects.get(user__username=follower_username)
    leader = UserProfile.objects.get(user=request.user)
    oneonone_meetings = OneOnOneMeeting.objects.filter(leader=leader)
    pdi_meetings = PdiMeeting.objects.filter(leader=leader)
    context['one_on_ones'] = oneonone_meetings
    context['pdi_meetings'] = pdi_meetings
    # pdi_meeting = PdiMeeting.objects.get_object_or_404(id= pdi_meeting_id)
    # pdi_plan_formset = PdiPlanFormset(instance=pdi_meeting)
    # pdi_plan_formset = PdiPlanFormset()
    # pdi_action_formset = ActionPlanFormset
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

                # action_plan_formset = ActionPlanFormset(saved_plan.actionplan_set)
                # saved_actions = action_plan_formset.save(commit=False)
                # for action in saved_actions:
                #     saved_action = action.save(commit=False)
                #     saved_action.pdi_plan = saved_plan
                #     saved_action.save()
            return redirect('/events')
    occupations = Occupation.objects.all()      
    skills      = Skill.objects.all()
    form = PdiMeetingForm(instance=follower)
    context['form'] = form
    context['plan_formset'] = PdiPlanFormset(prefix='planformset')
    context['occupations'] = occupations
    context['skills'] = skills
    context['follower'] = follower
    return render(request, template_name=template, context=context)

def edit_pdi_meeting(request, follower_username):
    template = 'core/pdi_meeting_update.html'
    context = {}
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


def pdi_meeting_evaluate(request, follower_username):
    template = 'core/pdi_meeting_evaluate.html'
    context = {}
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
        # action_plan_formset = ActionPlanFormset(request.POST, request.FILES, prefix='actionplanformset35')
        for plan in pdi_plans:
            # action_plan_formset = ActionPlanStatusFormset(prefix='actionplanformset'+str(plan.id), instance=plan)
            action_plan_form = ActionPlanStatusForm(request.POST, request.FILES)
            if action_plan_form.is_valid():
                saved_form = action_plan_form.save(commit=False)
                saved_form.pdi_plan_id = plan.id
                saved_form.save()
            # for form in action_plan_formset:
                # if form.is_valid():
                #     form.save()
        return redirect('core:team')
        # pdi_form  = PdiMeetingForm(request.POST)
        # plan_formset = PdiPlanFormset(request.POST, request.FILES, prefix='planformset')
        # if plan_formset.is_valid() and pdi_form.is_valid():
        #     saved_pdi_meeting = pdi_form.save(commit=False)
        #     saved_pdi_meeting.follower = follower
        #     saved_pdi_meeting.leader = leader
        #     saved_pdi_meeting.save()
        #     saved_plans = plan_formset.save(commit=False)
        #     for saved_plan in saved_plans:
        #         saved_plan.pdi_meeting = saved_pdi_meeting
        #         saved_plan.save()
        #         for plan in plan_formset:
        #             for nested in plan.nested:
        #                 nested.save(commit=False)
        #                 nested.pdi_plan = saved_plan
        #                 nested.save()
        #     return redirect('/team')
    return render(request, template_name=template, context=context)


@login_required(login_url='/accounts/login/')
def list_events(request):
    template = 'core/events.html'
    context = {}
    user      = UserProfile.objects.get(user=request.user)
    oneonone_meetings = OneOnOneMeeting.objects.filter(leader=user)
    pdi_meetings = PdiMeeting.objects.filter(leader=user)
    followers = []
    for meeting in oneonone_meetings:
        profile = UserProfile.objects.get(id= meeting.follower_id)
        if profile not in followers:
            followers.append(profile)
    context['one_on_ones'] = oneonone_meetings
    context['pdi_meetings'] = pdi_meetings
    context['followers'] = followers
    return render(request, template_name=template, context=context)




@login_required(login_url='/accounts/login/')
def show_team(request):
    template = 'core/team.html'
    context = {}
    user = UserProfile.objects.get(user=request.user)
    all_pdi_meetings = PdiMeeting.objects.filter(leader=user).order_by('-date_time')
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
    context['pdi_meetings'] = pdi_meetings
    context['followers'] = followers
    return render(request, template_name=template, context=context)



def meeting_evaluation(request, meeting_id, meeting_type):
    pdi_meeting = None
    one_on_one = None
    template = 'core/meeting_evaluation.html'
    context = {}
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