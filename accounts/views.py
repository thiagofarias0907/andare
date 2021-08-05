import os

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from .forms import UserForm, UserProfileForm, UserProfilePictureForm

# Create your views here.
from .models import UserProfile


def add_user(request):
    template = 'accounts/add_user.html'
    context = {}
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.set_password(f.password)
            f.save()
            user_profile = UserProfile.objects.create(user=User.objects.get(username=f.username))
            user_profile.save()
            messages.success(request,"Usuário cadastrado com sucesso!")
        else:
            messages.error(request, "Falha no cadastro de usuário!")
    form = UserForm()
    context['form'] = form
    return render(request, template, context)

def user_login(request):
    template = 'accounts/user_login.html'
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next','/'))
        else:
            messages.error(request, "Usuário ou senha inválidos")
    return render(request, template, context)

@login_required(login_url='/accounts/login/')
def user_logout(request):
    logout(request)
    return redirect('accounts:user_login')


@login_required(login_url='/accounts/login/')
def user_change_password(request):
    template = 'accounts/user_change_password.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Senha alterada com sucesso!')
        else:
            messages.error(request,'Não foi possível alterar a senha')
    form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render(request,template,context)

@login_required(login_url='/accounts/login/')
def change_user_profile(request):
    template = 'accounts/change_user_profile.html'
    context = {}
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.user = request.user
            form_save.save()
            messages.success(request, "Perfil alterado com Sucesso")
        else:
            messages.error(request, 'Não foi possível alterar o perfil')
    form = UserProfileForm()
    context['form'] = form
    return render(request,template,context)

@login_required(login_url='/accounts/login/')
def update_user_profile_picture(request, username):
    template = 'accounts/change_user_profile.html'
    context = {}
    profile = UserProfile.objects.get(user__username=username)
    if request.method == 'POST':
        form = UserProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso")
        else:
            messages.error(request, 'Não foi possível atualizar o perfil')
    form = UserProfilePictureForm(instance=profile)
    context['form'] = form
    context['username'] = username
    return render(request,template,context)

@login_required(login_url='/accounts/login/')
def profile(request, username):
    template = 'accounts/profile.html'
    context = {}
    profile = UserProfile.objects.get(user__username=username)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.user = request.user
            form_save.save()
            messages.success(request, "Perfil alterado com Sucesso")
        else:
            messages.error(request, 'Não foi possível alterar o perfil')
    form = UserProfileForm(instance=profile)
    context['form'] = form
    context['username'] = username
    return render(request,template,context)