from django.urls import path

app_name = 'core'

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('one_on_one/', views.one_on_one, name='one_on_one'),
    path('one_on_one/<follower>', views.one_on_one_follower, name='one_on_one_follower'),
    path('one_on_one/<leader_username>/<follower_username>', views.update_one_on_one, name='update_one_on_one'),
    path('pdi_meeting/<follower_username>', views.pdi_meeting, name='pdi_meeting'),
    path('edit_pdi_meeting/<follower_username>', views.edit_pdi_meeting, name='edit_pdi_meeting'),
    path('evaluate/<meeting_type>/<int:meeting_id>', views.meeting_evaluation, name='meeting_evaluation'),
    # path('pdi_meeting/evaluate/<follower_username>', views.pdi_meeting_evaluate, name='pdi_meeting_evaluate'),
    path('events/', views.list_events, name='events'),
    path('team/', views.show_team, name='team'),
    path('career/', views.list_events, name='career'),
]