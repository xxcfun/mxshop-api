from django.apps import AppConfig


class UserOperationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_operation'
    verbose_name = '操作管理'

    def ready(self):
        import user_operation.signals
