from career.models import *
from core.models import *

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.db.models import Q

from core.views import get_next_events

def has_leader_profile(user):
    if UserProfile.objects.get(user = user).profile == 2:
        return True
    return False

# @login_required(login_url='/accounts/login/')
# def pie_chart(request):
#     labels = []
#     data = []
#     occupations = Occupation.objects.all()
#     users = UserProfile.objects.all()
#     for occupation in occupations:
#         count = 0
#         for user in users:
#             if user.occupation == occupation:
#                 count = count + 1    
#         labels.append(occupation.name)
#         data.append(count)

#     return render(request, 'dashboard/chart.html', {
#         'labels': labels,
#         'data': data,
#     })

@login_required(login_url='/accounts/login/')
def dashboard(request):
    this_profile = UserProfile.objects.get(user=request.user)
    is_leader = has_leader_profile(request.user)
    context = get_next_events(user=request.user)
    occupation_pie_chart_data = {
        'data': [],
        'labels': [],
    }
    pdi_meetings_bar_chart_data = {
        'data': [],
        'labels': [],
    }
    pdi_completed_bar_chart_data = {
        'data': [],
        'labels': [],
    }
    status_bar_chart_data = {
        'data': [],
        'labels': [],
    }
    
    evaluation_score_bar_chart_data = {
        'data': [],
        'labels': [],
    }
    
    evaluation_feelings_bar_chart_data = {
        'data': [],
        'labels': [],
    }
    # projecthistory_timeline_chart_data = {
    #     'data': [],
    #     'labels': []
    # }

    selected_occupation = 0 
    if request.GET.get('occupation') != '' and request.GET.get('occupation') is not None:
        selected_occupation = int(request.GET.get('occupation'))

    occupations = Occupation.objects.all()
    users = UserProfile.objects.all()
    for occupation in occupations:
        count = 0
        for user in users:
            if user.occupation is None:
                continue 
            if user.occupation.id == occupation.id:
                count = count + 1    
        occupation_pie_chart_data.get('labels').append(occupation.name+' ' + str(occupation.level))
        occupation_pie_chart_data.get('data').append(count)

    if is_leader:
        pdi_meetings = PdiMeeting.objects.all()
        for user in users:
            count = 0
            name = user.user.first_name
            for pdi_meeting in pdi_meetings:
                if user.id == pdi_meeting.follower.id:
                    count = count + 1
            pdi_meetings_bar_chart_data.get('data').append(count)
            pdi_meetings_bar_chart_data.get('labels').append(name)
    else:
        pdi_meetings = PdiMeeting.objects.filter(follower = this_profile)
        name = this_profile.user.first_name
        count = 0
        for pdi_meeting in pdi_meetings:
            if this_profile == pdi_meeting.follower:
                count = count + 1
        pdi_meetings_bar_chart_data.get('data').append(count)
        pdi_meetings_bar_chart_data.get('labels').append(name)

    if is_leader:
        for user in users:
            count = 0
            completed = 0
            total_actions = 0
            name = user.user.first_name
            pdi_meetings = PdiMeeting.objects.filter(follower=user)
            for pdi_meeting in pdi_meetings:
                if user.id == pdi_meeting.follower.id:
                    count = count + 1
                plans = PdiPlan.objects.filter(pdi_meeting=pdi_meeting)
                for plan in plans:
                    action_plans = ActionPlan.objects.filter(pdi_plan=plan)
                    for action in action_plans:
                        total_actions = total_actions + 1
                        if action.status == 4:
                            completed = completed + 1
            if (total_actions>0):
                pdi_completed_bar_chart_data.get('data').append(round(100*completed/total_actions,2))
            else:
                pdi_completed_bar_chart_data.get('data').append(0)
            pdi_completed_bar_chart_data.get('labels').append(name)
    else:
        count = 0
        completed = 0
        total_actions = 0
        name = this_profile.user.first_name
        pdi_meetings = PdiMeeting.objects.filter(follower=this_profile)
        for pdi_meeting in pdi_meetings:
            if this_profile == pdi_meeting.follower:
                count = count + 1
            plans = PdiPlan.objects.filter(pdi_meeting=pdi_meeting)
            for plan in plans:
                action_plans = ActionPlan.objects.filter(pdi_plan=plan)
                for action in action_plans:
                    total_actions = total_actions + 1
                    if action.status == 4:
                        completed = completed + 1
        if (total_actions>0):
            pdi_completed_bar_chart_data.get('data').append(round(100*completed/total_actions,2))
        else:
            pdi_completed_bar_chart_data.get('data').append(0)
        pdi_completed_bar_chart_data.get('labels').append(name)

    # for user in users:
    #     count = 0
    #     name = user.user.first_name
    #     action_plans = ActionPlan.objects.filter(user=user)
    #     for action in action_plans:
    #         if action.status == 4:
    #             count = count + 1
    #     if (len(action_plans)>0):
    #         pdi_completed_bar_chart_data.get('data').append(count/len(action_plans))
    #     else:
    #         pdi_completed_bar_chart_data.get('data').append(0)
    #     pdi_completed_bar_chart_data.get('labels').append(name)


    if is_leader:
        pdi_meetings = PdiMeeting.objects.filter(leader=this_profile)
    status_choices = ActionPlan.STATUS_CHOICES
    for status in status_choices:
        count = 0
        for meeting in pdi_meetings:
            plans =  PdiPlan.objects.filter(pdi_meeting=meeting)
            for plan in plans:
                action_plans = ActionPlan.objects.filter(pdi_plan=plan)
                for action in action_plans:
                    if action.status == status[0]:
                        count = count + 1
        status_bar_chart_data.get('data').append(count)
        status_bar_chart_data.get('labels').append(status[1])



    if is_leader:
        evaluations = MeetingEvaluation.objects.all()
    else:
        evaluations = MeetingEvaluation.objects.filter(user_profile=this_profile)

    emoji_choices = MeetingEvaluation.EMOJI_CHOICES
    for feeling in emoji_choices:
        feeling_count = 0
        for evaluation in evaluations:
            if evaluation.feeling == feeling[0]:
                feeling_count = feeling_count + 1
        evaluation_feelings_bar_chart_data.get('data').append(feeling_count)
        evaluation_feelings_bar_chart_data.get('labels').append(feeling[2])


    if is_leader:
        for user in users:
            evaluations = MeetingEvaluation.objects.filter(user_profile=user)
            sum = 0
            count = 0
            avg = 0
            for evaluation in evaluations:
                sum = sum + evaluation.score
                count = count +1
            if count > 0:
                avg = round(sum/count,2)
            evaluation_score_bar_chart_data.get('data').append(avg)
            evaluation_score_bar_chart_data.get('labels').append(user.user.first_name)
    else:
        sum = 0
        count = 0
        avg = 0
        for evaluation in evaluations:
            sum = sum + evaluation.score
            count = count +1
        if count > 0:
            avg = round(sum/count,2)
        evaluation_score_bar_chart_data.get('data').append(avg)
        evaluation_score_bar_chart_data.get('labels').append(user.user.first_name)

    # colors= ['#FFF07C', '#80FF72', '#7EE8FA', '#EEC0C6', '#E58C8A']
    # users_history = ProjectHistory.objects.filter().order_by('id')
    # labels = [] 
    # for project_history in users_history:
    #     if project_history.date not in labels:
    #         labels.append(project_history.date)

    # i = 0
    # for user in users:
    #     data = []
    #     dataset = []
    #     print(user.id)
    #     last_pdi_meeting = 0
    #     for project_history in users_history:
    #         if user.id == project_history.project_id:
    #             last_pdi_meeting = project_history.pdi_meeting_id
    #             data.append(project_history.pdi_meeting_id)
    #         else:
    #             data.append(last_pdi_meeting)
    #     dataset = {'data':data,'labels':labels, 'color': colors[int((i)%len(colors))], 'name':user.name}
    #     projecthistory_timeline_chart_data.get('data').append(dataset)
    #     i = i + 1        

    # colors= ['#FFF07C', '#80FF72', '#7EE8FA', '#EEC0C6', '#E58C8A']
    # users_history = ProjectHistory.objects.filter().order_by('id')
    # i = 0
    
    # from datetime import date, timedelta
    # today = date.today() 
    # labels=[]
    # for i in range(1,32):
    #    date_iter = today - timedelta(30-i)
    #    labels.append(date_iter)     
    #    projecthistory_timeline_chart_data.get('labels').append(date_iter)
    
    # users_counter = 0
    # for user in users:
    #     if user.occupation_id != selected_occupation and selected_occupation > 0:
    #         continue
    #     users_counter =  users_counter +1
    #     data = []
    #     dataset = []
    #     last_pdi_meeting_order = 0
    #     users_history = ProjectHistory.objects.filter(project_id=user.id)
    #     last_date = today - timedelta(31)
    #     for project_history in users_history:
    #         for label in labels:
    #             if label == project_history.date:
    #                 last_date = label
    #                 for pdi_meeting in pdi_meetings:
    #                     if pdi_meeting.id == project_history.pdi_meeting_id:
    #                         last_pdi_meeting_order = pdi_meeting.order
    #                         data.append(last_pdi_meeting_order)
    #             elif (label < project_history.date) and (label > last_date):
    #                 data.append(last_pdi_meeting_order)
    #                 last_date = label
                
    #     if len(data) == 0:
    #         data = [0 for i in range(0,31)]
    #     dataset = {'data':data, 'color': colors[int((i)%len(colors))], 'name':user.name}
    #     projecthistory_timeline_chart_data.get('data').append(dataset)
    #     i = i + 1  

    # if selected_occupation > 0:
    #     active_users = UserProfile.objects.filter(Q(status=1)|Q(status=2),Q(occupation_id=selected_occupation))
    #     inactive_users = UserProfile.objects.filter(Q(status=4),Q(occupation_id=selected_occupation))
    #     done_users = UserProfile.objects.filter(Q(status=3),Q(occupation_id=selected_occupation))
    
    # if selected_occupation == 0 or selected_occupation is None:
    #     active_users = UserProfile.objects.filter(Q(status=1)|Q(status=2))
    #     inactive_users = UserProfile.objects.filter(Q(status=4))
    #     done_users = UserProfile.objects.filter(Q(status=3))

    if is_leader:
        pdi_meetings_qty = len(PdiMeeting.objects.all())
        one_on_ones_qty = len(OneOnOneMeeting.objects.all())
        followers_qty = len(UserProfile.objects.filter(creator__user=request.user))
        plans_qty = len(PdiPlan.objects.all())
        actionplans_qty = len(ActionPlan.objects.all())
    else:
        pdi_meetings_qty = len(pdi_meetings)
        one_on_ones_qty = len(OneOnOneMeeting.objects.filter(follower=this_profile))
        followers_qty = 0
        plans_qty = len(PdiPlan.objects.filter(pdi_meeting__follower=this_profile))
        actionplans_qty = len(ActionPlan.objects.filter(pdi_plan__pdi_meeting__follower=this_profile))

    
    context = get_next_events(user=request.user)

    context['pdi_meetings_bar_chart_data'] = pdi_meetings_bar_chart_data
    context['status_bar_chart_data'] = status_bar_chart_data
    context['occupation_pie_chart_data'] = occupation_pie_chart_data 
    context['pdi_completed_bar_chart_data'] = pdi_completed_bar_chart_data
    context['evaluation_score_bar_chart_data'] = evaluation_score_bar_chart_data
    context['evaluation_feelings_bar_chart_data'] = evaluation_feelings_bar_chart_data
    # context['projecthistory_timeline_chart_data'] = projecthistory_timeline_chart_data
    context['occupations'] = occupations
    context['selected_occupation'] = selected_occupation
    #context['users_qty'] = (len(active_users) + len(inactive_users) + len(done_users))
    #context['active_users'] = len(active_users)
    #context['inactive_users'] = len(inactive_users)
    #context['done_users'] = len(done_users)
    context['users'] = len(users)
    context['pdi_meetings_qty'] = pdi_meetings_qty
    context['one_on_ones_qty' ] = one_on_ones_qty
    context['followers_qty'   ] = followers_qty
    context['plans_qty'       ] = plans_qty
    context['actionplans_qty' ] = actionplans_qty
    #context['team'] = len(team)
    context['pdi_meetings'] = pdi_meetings
    context['is_leader'] = is_leader
    if is_leader:
        template = 'dashboard/dashboard.html'
    else:
        template = 'dashboard/follower_dashboard.html'

    return render(request, template_name=template, context=context)

@login_required(login_url='/accounts/login/')
def home(request):
    template = 'dashboard/dashboard.html'
    context = get_next_events(user=request.user)
    users = UserProfile.objects.all()
    context['users']= users
    return render(request, template_name=template, context=context)

