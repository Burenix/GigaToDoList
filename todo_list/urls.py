from django.urls import path

from .views import TaskList

urlpatterns = [
    path('main/', TaskList.as_view(), name='tasks'),
]