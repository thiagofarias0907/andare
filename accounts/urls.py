from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('add_user/', views.add_user, name ='add_user'),
    path('login/', views.user_login, name ='user_login'),
    path('logout/', views.user_logout, name ='user_logout'),
    path('change_password/', views.user_change_password, name ='change_password'),
    path('change_profile/', views.change_user_profile, name='change_profile'),
    path('update_profile/<username>', views.update_user_profile_picture, name='update_profile'),
    path('profile/<username>', views.profile, name='profile'),
]