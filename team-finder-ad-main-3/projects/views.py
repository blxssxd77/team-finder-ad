from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from team_finder.pagination import get_page
from users.models import User

from .constants import STATUS_CLOSED, STATUS_OPEN
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
    page = get_page(projects, request)
    return render(request, 'projects/project_list.html', {
        'projects': page.object_list,
        'page_obj': page,
    })


def project_detail(request, project_id):
    _prefetch_user_favorites(request)
    project = get_object_or_404(
        Project.objects.select_related('owner').prefetch_related('participants'),
        pk=project_id,
    )
    return render(request, 'projects/project-details.html', {'project': project})


@login_required
@require_http_methods(['GET', 'POST'])
def project_create(request):
    form = ProjectForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'projects/create-project.html', {
            'form': form,
            'is_edit': False,
        })
    project = form.save(commit=False)
    project.owner = request.user
    project.save()
    project.participants.add(request.user)
    return redirect('projects:detail', project_id=project.pk)


@login_required
@require_http_methods(['GET', 'POST'])
def project_edit(request, project_id):
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    form = ProjectForm(request.POST or None, instance=project)
    if not form.is_valid():
        return render(request, 'projects/create-project.html', {
            'form': form,
            'is_edit': True,
        })
    form.save()
    return redirect('projects:detail', project_id=project.pk)


@login_required
@require_POST
def project_complete(request, project_id):
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    if project.status != STATUS_OPEN:
        return JsonResponse(
            {'status': 'error'},
            status=HTTPStatus.BAD_REQUEST,
        )
    project.status = STATUS_CLOSED
    project.save()
    return JsonResponse({'status': 'ok', 'project_status': project.status})


@login_required
@require_POST
def toggle_participate(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner == request.user:
        return JsonResponse(
            {'status': 'error'},
            status=HTTPStatus.BAD_REQUEST,
        )
    is_participant = project.participants.filter(pk=request.user.pk).exists()
    if is_participant:
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)
    return JsonResponse({'status': 'ok', 'participant': not is_participant})


@login_required
@require_POST
def toggle_favorite(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    favorited = request.user.favorites.filter(pk=project.pk).exists()
    if favorited:
        request.user.favorites.remove(project)
    else:
        request.user.favorites.add(project)
    return JsonResponse({'status': 'ok', 'favorited': not favorited})


@login_required
def favorites_list(request):
    _prefetch_user_favorites(request)
    projects = request.user.favorites.select_related('owner').prefetch_related(
        'participants',
    )
    page = get_page(projects, request)
    return render(request, 'projects/favorite_projects.html', {
        'projects': page.object_list,
        'page_obj': page,
    })
