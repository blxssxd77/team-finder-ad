from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from team_finder.pagination import get_page

from .forms import (
    CustomPasswordChangeForm,
    LoginForm,
    ProfileEditForm,
    RegistrationForm,
)
from .models import User


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.user.is_authenticated:
        return redirect('projects:list')
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('users:login')
    return render(request, 'users/register.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('projects:list')
    form = LoginForm(request, data=request.POST or None)
    if form.is_valid():
        auth.login(request, form.get_user())
        return redirect('projects:list')
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    auth.logout(request)
    return redirect('projects:list')


def user_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'users/user-details.html', {'user': user})


@login_required
@require_http_methods(['GET', 'POST'])
def edit_profile(request):
    form = ProfileEditForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user,
    )
    if form.is_valid():
        form.save()
        return redirect('users:detail', user_id=request.user.pk)
    return render(request, 'users/edit_profile.html', {
        'form': form,
        'user': request.user,
    })


@login_required
@require_http_methods(['GET', 'POST'])
def change_password(request):
    form = CustomPasswordChangeForm(request.user, request.POST or None)
    if form.is_valid():
        form.save()
        auth.update_session_auth_hash(request, form.user)
        return redirect('users:detail', user_id=request.user.pk)
    return render(request, 'users/change_password.html', {'form': form})


def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    active_filter = request.GET.get('filter', '')

    if request.user.is_authenticated and active_filter:
        if active_filter == 'owners-of-favorite-projects':
            users = users.filter(
                owned_projects__interested_users=request.user,
            ).distinct()
        elif active_filter == 'owners-of-participating-projects':
            users = users.filter(
                owned_projects__participants=request.user,
            ).exclude(pk=request.user.pk).distinct()
        elif active_filter == 'interested-in-my-projects':
            users = users.filter(
                favorites__owner=request.user,
            ).distinct()
        elif active_filter == 'participants-of-my-projects':
            users = users.filter(
                participated_projects__owner=request.user,
            ).exclude(pk=request.user.pk).distinct()

    page = get_page(users, request)
    return render(request, 'users/participants.html', {
        'participants': page.object_list,
        'active_filter': active_filter,
        'page_obj': page,
    })
