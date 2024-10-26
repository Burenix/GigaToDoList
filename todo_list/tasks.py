from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from .models import Task

@shared_task
def send_task_reminders():
    # Получаем задачи с напоминаниями
    tasks = Task.objects.filter(status=False, deadline__gt=now(), reminder_sent=False)
    for task in tasks:
        reminder_time = task.deadline - task.reminder_time
        if reminder_time <= now():
            # Отправляем email-напоминание
            send_mail(
                'Напоминание о задаче',
                f'Привет, {task.user.username}! Напоминаем о задаче: {task.title}, срок выполнения: {task.deadline}.',
                'jokeryt.fix@yandex.ru',
                [task.user.email],
                fail_silently=False,
            )
            # Обновляем статус, чтобы не отправлять повторно
            task.reminder_sent = True
            task.save()