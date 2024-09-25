from django.urls import path

from .views import TaskCreate, TaskList

urlpatterns = [
    path('main/', TaskList.as_view(), name='tasks'),
    path('main/create-task/', TaskCreate.as_view(), name='task-create'),
]