from django.urls import path

from .views import TaskCreate, TaskDetail, TaskList

urlpatterns = [
    path('main/', TaskList.as_view(), name='tasks'),
    path('main/create-task/', TaskCreate.as_view(), name='task-create'),
    path('main/detail-task/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
]