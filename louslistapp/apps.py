from django.apps import AppConfig


class LouslistappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'louslistapp'

    def ready(self):
        import louslistapp.signals