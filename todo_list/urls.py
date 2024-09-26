from django.urls import path

from .views import TaskCreate, TaskDelete, TaskDetail, TaskList, TaskUpdate

urlpatterns = [
    path('main/', TaskList.as_view(), name='tasks'),
    path('main/create-task/', TaskCreate.as_view(), name='task-create'),
    path('main/detail-task/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
    path('main/delete-task/<int:pk>/', TaskDelete.as_view(), name='task-delete'),
    path('main/update-task/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
]