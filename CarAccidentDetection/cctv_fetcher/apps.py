from django.apps import AppConfig


class CctvFetcherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cctv_fetcher'

    # def ready(self):
    #     from .scheduler import start
    #     start()
