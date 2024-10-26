from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Устанавливаем переменную окружения с настройками Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'giga_todo_list.settings')

# Создаем экземпляр Celery
app = Celery('giga_todo_list')

# Загружаем настройки из конфигурационного файла Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически регистрируем задачи из приложений Django
app.autodiscover_tasks()