from django.apps import AppConfig
from django.utils.module_loading import import_string  # Add this import
from django.db import connection

class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'

    def ready(self):
        # Import the Session model lazily and check if the table exists
        Session = import_string('django.contrib.sessions.models.Session')

        # Check if the table 'django_session' exists before attempting to delete sessions
        if 'django_session' in connection.introspection.table_names():
            Session.objects.all().delete()