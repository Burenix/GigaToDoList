from django.urls import path

from todo_list.views import Search, TaskCreate, TaskDelete, TaskDetail, TaskFilter, TaskList, TaskUpdate

urlpatterns = [
    path('', TaskList.as_view(), name='tasks'),
    path('create-task/', TaskCreate.as_view(), name='task-create'),
    path('detail-task/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
    path('delete-task/<int:pk>/', TaskDelete.as_view(), name='task-delete'),
    path('update-task/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    
    path('search/', Search.as_view(), name='task-search'),
    path('filter/', TaskFilter.as_view(), name='task-filter'),
]