# Generated by Django 5.1.1 on 2024-11-03 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_list', '0002_task_reminder_sent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='complexity',
        ),
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=1),
            preserve_default=False,
        ),
    ]
