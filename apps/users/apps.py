from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = '用户管理'

    # 子类可以覆盖此方法来执行初始化任务,例如注册信号
    def ready(self):
        import users.signals
