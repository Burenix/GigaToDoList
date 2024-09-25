from django.shortcuts import render
from django.views.generic import edit
from django.views import generic

from .models import Task

# Create your views here.
class TaskList(generic.ListView):
    model = Task
    template_name = 'todo_list/main.html'
    context_object_name = 'tasks'