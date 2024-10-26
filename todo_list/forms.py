from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'reminder_time', 'complexity']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'class': 'flatpickr'}),
        }