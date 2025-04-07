from django.conf import settings

from ultralytics import YOLO


class ModelRegistry:
    _model = None

    @classmethod
    def get_model(cls):
        return cls._model

    @classmethod
    def load_model(cls):
        if cls._model is None:
            model_path = settings.BASE_DIR / 'main' / 'cv_model_pt_files' / 'accident_detection.pt'
            cls._model = YOLO(model_path)
