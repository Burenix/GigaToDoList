# Generated by Django 5.1.1 on 2024-10-07 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_list', '0002_task_reminder_time_task_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='complexity',
            field=models.IntegerField(choices=[(1, 'Easy'), (2, 'Medium'), (3, 'Hard'), (4, 'Very hard'), (5, 'Impossible')], default=1),
            preserve_default=False,
        ),
    ]
