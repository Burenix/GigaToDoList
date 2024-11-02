from django.urls import path

from todo_list.views import TaskCreate, TaskDelete, TaskDetail, TaskList, TaskUpdate

urlpatterns = [
    path('', TaskList.as_view(), name='tasks'),
    path('create-task/', TaskCreate.as_view(), name='task-create'),
    path('detail-task/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
    path('delete-task/<int:pk>/', TaskDelete.as_view(), name='task-delete'),
    path('update-task/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    
    path('search/', TaskList.as_view(), name='task-search'),
    path('filter/', TaskList.as_view(), name='task-filter'),
]