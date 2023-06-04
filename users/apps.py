from django.apps import AppConfig
# from django_cron.registry import CronJobRegistry


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

# class UsersConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'users'

#     def ready(self):
#         from users.tasks import DeleteOldFilesCronJob
#         self.register_cron_jobs([DeleteOldFilesCronJob])