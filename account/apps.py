from django.apps import AppConfig

class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    # def ready(self):
    #     # Import and register your signals here
    #     from account.signals import create_username  # Import your signal
    def ready(self):
        import account.signals