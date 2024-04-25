from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_task, name='add_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('change_status/<int:task_id>/', views.change_status, name='change_status'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
]
