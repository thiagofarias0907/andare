import os

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from .forms import UserForm, UserProfileForm, UserProfilePictureForm, UserFormset

from .models import UserProfile

from core.views import get_next_events

def add_user(request):
    template = 'accounts/add_user.html'
    context = get_next_events(user=request.user)
    creator = UserProfile.objects.get(user= request.user)
    if request.method == 'POST':
        form = UserForm(request.POST)
        formset = UserFormset(request.POST, request.FILES, prefix='formset')
        if form.is_valid() and formset.is_valid():
            f = form.save(commit=False)
            f.set_password(f.password)
            f.save()
            for form in formset:
                saved_profile_form = form.save(commit=False)
                saved_profile_form.creator = creator
                saved_profile_form.user = f
                saved_profile_form.save()
            messages.success(request,"Usuário cadastrado com sucesso!")
        else:
            messages.error(request, "Falha no cadastro de usuário!")
    form = UserForm()
    formset = UserFormset(prefix='formset')
    context['form'] = form
    context['formset'] = formset
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
    context = get_next_events(user=request.user)
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
    context = get_next_events(user=request.user)
    profile = UserProfile.objects.get(user=request.user)
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
    context['profile'] = profile
    return render(request,template,context)

@login_required(login_url='/accounts/login/')
def update_user_profile_picture(request, username):
    template = 'accounts/change_user_profile.html'
    context = get_next_events(user=request.user)
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
    context['profile'] = profile
    return render(request,template,context)

@login_required(login_url='/accounts/login/')
def profile(request, username):
    template = 'accounts/profile.html'
    context = get_next_events(user=request.user)
    profile_update = UserProfile.objects.get(user__username = username)
    profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.id = profile_update.id
            form_save.user = profile_update.user
            form_save.picture = profile_update.picture
            form_save.save()
            messages.success(request, "Perfil alterado com Sucesso")
        else:
            messages.error(request, 'Não foi possível alterar o perfil')
    form = UserProfileForm(instance=profile_update)
    context['form'] = form
    context['username'] = username
    context['profile_update'] = profile_update
    context['profile_type'] = profile.profile
    return render(request,template,context)