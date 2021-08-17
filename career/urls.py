from django.urls import path

app_name = 'career'

from . import views

urlpatterns = [
    path('', views.list_all, name='list_career'),
    path('add/', views.add_occupation, name='add_occupation'),
    path('edit/<int:occupation_id>', views.edit_occupation, name='edit_occupation'),
    path('delete/<int:occupation_id>/', views.delete_occupation, name='delete_occupation'),
]