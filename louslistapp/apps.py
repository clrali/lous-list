from django.apps import AppConfig


class LouslistappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'louslistapp'

# class UsersConfig(AppConfig):
#     name = 'users'
 
#     def ready(self):
#         import users.signals
