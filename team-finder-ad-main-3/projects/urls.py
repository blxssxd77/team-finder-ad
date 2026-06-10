from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('list/', views.project_list, name='list'),
    path('favorites/', views.favorites_list, name='favorites'),
    path('create-project/', views.project_create, name='create'),
    path('<int:pk>/', views.project_detail, name='detail'),
    path('<int:pk>/edit/', views.project_edit, name='edit'),
    path('<int:pk>/complete/', views.project_complete, name='complete'),
    path('<int:pk>/toggle-participate/', views.toggle_participate, name='toggle_participate'),
    path('<int:pk>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
]
