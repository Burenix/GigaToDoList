from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
from django.forms import ValidationError
import pytz

COMPLEXITY_CHOICES = (
    (1, 'Low'),
    (2, 'Medium'),
    (3, 'High'),
)

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=52)
    description = models.TextField(max_length=252)
    status = models.BooleanField(default=False)
    deadline = models.DateTimeField()
    reminder_time = models.DurationField(default=timedelta(hours=1))
    task_created = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(choices=COMPLEXITY_CHOICES)
    reminder_sent = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
    
    def clean(self):
        moscow_tz = pytz.timezone('Europe/Moscow')

        # Проверка deadline
        if self.deadline < datetime.now(moscow_tz):
            raise ValidationError('Срок выполнения не может быть в прошлом.')
        
        # Проверка reminder_time
        if self.reminder_time > (self.deadline - datetime.now(moscow_tz)):
            raise ValidationError('Время напоминания не может быть после срока выполнения.')
        
        return super().clean()

    class Meta:
        ordering = ['status']