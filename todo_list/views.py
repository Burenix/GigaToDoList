from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import generic

from todo_list.models import Task

################### CRUD ###################

class TaskList(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = 'todo_list/main.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        """
        Возвращает список задач только для текущего авторизованного пользователя.
        """
        return Task.objects.filter(user=self.request.user)

class TaskCreate(LoginRequiredMixin, generic.CreateView):
    model = Task
    fields = ['title', 'description', 'complexity', 'deadline', 'reminder_time']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        """
        При успешном создании задачи устанавливает пользователя, который создал задачу.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskDetail(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Task

    def test_func(self):
        """
        Проверяет, совпадает ли пользователь, просматривающий детальную информацию о задаче, с пользователем, 
        который создал эту задачу.
        """
        return super().get_object().user == self.request.user

class TaskDelete(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')

    def test_func(self):
        """
        Проверяет, совпадает ли пользователь, удаляющий задачу, с пользователем, 
        который создал эту задачу.
        """
        return super().get_object().user == self.request.user

class TaskUpdate(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Task
    fields = ['title', 'description', 'status', 'deadline', 'reminder_time']
    success_url = reverse_lazy('tasks')

    def test_func(self):
        """
        Проверяет, совпадает ли пользователь, обновляющий задачу, с пользователем, 
        который создал эту задачу.
        """
        return super().get_object().user == self.request.user

################### CRUD ###################

################## SEARCH ##################

class Search(LoginRequiredMixin, generic.ListView):
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

class TaskFilter(LoginRequiredMixin, generic.ListView):
    template_name = 'todo_list/main.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = Task.objects.all()

        filter = self.request.GET.get('filter', 'all') 

        if filter == 'complete':
            return queryset.filter(status__exact=True)
        elif filter == 'incomplete':
            return queryset.filter(status__exact=False)
        elif filter == 'deadline':
            return queryset.filter(status__exact=False).order_by('deadline')
        elif filter == 'simple':
            return queryset.filter(status__exact=False).order_by('complexity')
        elif filter == 'difficult':
            return queryset.filter(status__exact=False).order_by('-complexity')
        else:
            return queryset  

################## FILTER ##################