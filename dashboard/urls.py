from django.urls import path, include

app_name = 'dashboard'

from . import views


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
]