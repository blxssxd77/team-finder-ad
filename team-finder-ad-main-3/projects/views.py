from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from users.models import User

from .forms import ProjectForm
from .models import Project


def _prefetch_user_favorites(request):
    if request.user.is_authenticated:
        request.user = User.objects.prefetch_related('favorites').get(
            pk=request.user.pk,
        )


def project_list(request):
    _prefetch_user_favorites(request)
    projects = Project.objects.select_related('owner').prefetch_related('participants')
    paginator = Paginator(projects, 12)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'projects/project_list.html', {
        'projects': page.object_list,
        'page_obj': page,
    })


def project_detail(request, pk):
    _prefetch_user_favorites(request)
    project = get_object_or_404(
        Project.objects.select_related('owner').prefetch_related('participants'),
        pk=pk,
    )
    return render(request, 'projects/project-details.html', {'project': project})


@login_required
@require_http_methods(['GET', 'POST'])
def project_create(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)
        return redirect('projects:detail', pk=project.pk)
    return render(request, 'projects/create-project.html', {
        'form': form,
        'is_edit': False,
    })


@login_required
@require_http_methods(['GET', 'POST'])
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect('projects:detail', pk=project.pk)
    return render(request, 'projects/create-project.html', {
        'form': form,
        'is_edit': True,
    })


@login_required
@require_POST
def project_complete(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if project.status != Project.STATUS_OPEN:
        return JsonResponse({'status': 'error'}, status=400)
    project.status = Project.STATUS_CLOSED
    project.save()
    return JsonResponse({'status': 'ok', 'project_status': 'closed'})


@login_required
@require_POST
def toggle_participate(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.owner == request.user:
        return JsonResponse({'status': 'error'}, status=400)
    if project.participants.filter(pk=request.user.pk).exists():
        project.participants.remove(request.user)
        return JsonResponse({'status': 'ok', 'participant': False})
    project.participants.add(request.user)
    return JsonResponse({'status': 'ok', 'participant': True})


@login_required
@require_POST
def toggle_favorite(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user.favorites.filter(pk=project.pk).exists():
        request.user.favorites.remove(project)
        favorited = False
    else:
        request.user.favorites.add(project)
        favorited = True
    return JsonResponse({'status': 'ok', 'favorited': favorited})


@login_required
def favorites_list(request):
    _prefetch_user_favorites(request)
    projects = request.user.favorites.select_related('owner').prefetch_related(
        'participants',
    )
    paginator = Paginator(projects, 12)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'projects/favorite_projects.html', {
        'projects': page.object_list,
        'page_obj': page,
    })
