from django.apps import AppConfig

class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'

    def ready(self):
        # Use lazy import of Session and the logout function to avoid app registry issues
        from django.utils.module_loading import import_string
        
        # Get the Session model after the app registry is ready
        Session = import_string('django.contrib.sessions.models.Session')
        
        # Delete all sessions to log out users
        Session.objects.all().delete()
