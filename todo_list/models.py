from django.db import models

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=52)
    description = models.TextField(max_length=252)
    status = models.BooleanField(default=False)
    deadline = models.DateTimeField()
    task_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['status']