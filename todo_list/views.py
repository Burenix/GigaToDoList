from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import edit
from django.views import generic

from .models import Task

################### CRUD ###################

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

################### CRUD ###################

################## SEARCH ##################

class Search(generic.ListView):
    template_name = 'todo_list/main.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(title__icontains=
                                   self.request.GET.get('search_text'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context
    
################## SEARCH ##################

################## FILTER ##################

class TaskFilter(generic.ListView):
    template_name = 'todo_list/main.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = Task.objects.all()

        filter = self.request.GET.get('filter')

        if filter == 'complete':
            return queryset.filter(status__exact=True)
        elif filter == 'incomplete':
            return queryset.filter(status__exact=False)
        elif filter == 'deadline':
            return queryset.filter(status__exact=False).order_by('deadline')
        else:
            return queryset
        

################## FILTER ##################