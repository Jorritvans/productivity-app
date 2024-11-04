from django.apps import AppConfig
from django.utils.module_loading import import_string
from django.db import connection


class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'

    def ready(self):
        # Import the Session model lazily and check if the table exists.
        Session = import_string('django.contrib.sessions.models.Session')

        # Ensure 'django_session' table exists before deleting sessions.
        if 'django_session' in connection.introspection.table_names():
            Session.objects.all().delete()
