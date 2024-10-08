from datetime import timedelta
from django.db import models
from django.conf import settings

COMPLEXITY_CHOICES = (
    (1, 'Easy'),
    (2, 'Medium'),
    (3, 'Hard'),
    (4, 'Very hard'),
    (5, 'Impossible'),
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
    complexity = models.IntegerField(choices=COMPLEXITY_CHOICES)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['status']