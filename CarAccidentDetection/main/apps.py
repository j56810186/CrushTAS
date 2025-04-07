# import some cv model framework
from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    # def ready(self):
    #     # Load the CV model (accident detection model) when the app is ready
    #     from .cv_model import ModelRegistry
    #     from .scheduler import start
    #     ModelRegistry.load_model()
    #     start()

