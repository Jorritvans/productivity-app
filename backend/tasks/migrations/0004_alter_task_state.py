# Generated by Django 4.2.16 on 2024-10-23 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_remove_task_attachment_remove_task_owners_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='state',
            field=models.CharField(choices=[('To-Do', 'To-Do'), ('In Progress', 'In Progress'), ('Done', 'Done')], max_length=50),
        ),
    ]