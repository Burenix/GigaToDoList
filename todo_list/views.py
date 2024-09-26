from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import edit
from django.views import generic

from .models import Task

# Create your views here.
class TaskList(generic.ListView):
    model = Task
    template_name = 'todo_list/main.html'
    context_object_name = 'tasks'

class TaskCreate(generic.CreateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')

class TaskDetail(generic.DetailView):
    model = Task

class TaskDelete(generic.DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')

class TaskUpdate(generic.UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')