from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from todo_list.forms import TaskForm
from todo_list.models import Task

################### CRUD ###################

class TaskList(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = 'todo_list/main.html'
    context_object_name = 'tasks'
    paginate_by = 5

    def get_queryset(self):
        """
        Возвращает отфильтрованный и отсортированный список задач для текущего авторизованного пользователя.
        """
        # Извлекаем исходный набор задач только для текущего пользователя
        queryset = Task.objects.filter(user=self.request.user)

        # Получаем выбранный фильтр и текст поиска из GET-запроса
        filter_value = self.request.GET.get('filter', 'all')
        
        search_text = self.request.GET.get('search_text')

        # Применяем фильтр
        if filter_value == 'complete':
            queryset = queryset.filter(status=True)
        elif filter_value == 'incomplete':
            queryset = queryset.filter(status=False)
        elif filter_value == 'deadline':
            queryset = queryset.filter(status=False).order_by('deadline')
        elif filter_value == 'low':
            queryset = queryset.filter(status=False).order_by('priority')
        elif filter_value == 'high':
            queryset = queryset.filter(status=False).order_by('-priority')

        # Применяем поиск, если указан текст поиска
        if search_text:
            queryset = queryset.filter(title__icontains=search_text)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Пагинация
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        try:
            tasks = paginator.page(page)
        except PageNotAnInteger:
            # Если 'page' не является целым числом, используем первую страницу
            tasks = paginator.page(1)
        except EmptyPage:
            # Если 'page' больше, чем количество страниц, используем последнюю страницу
            tasks = paginator.page(paginator.num_pages)

        context['tasks'] = tasks
        context['paginator'] = paginator
        context['page_obj'] = tasks

        return context

class TaskCreate(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
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
    form_class = TaskForm
    success_url = reverse_lazy('tasks')

    def test_func(self):
        """
        Проверяет, совпадает ли пользователь, обновляющий задачу, с пользователем, 
        который создал эту задачу.
        """
        return super().get_object().user == self.request.user

################### CRUD ###################