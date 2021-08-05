from django.urls import path

app_name = 'core'

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('one_on_one/', views.one_on_one, name='one_on_one'),
    path('one_on_one/<leader_username>/<follower_username>', views.update_one_on_one, name='update_one_on_one'),
    path('pdi_meeting/<follower_username>', views.pdi_meeting, name='pdi_meeting'),
]