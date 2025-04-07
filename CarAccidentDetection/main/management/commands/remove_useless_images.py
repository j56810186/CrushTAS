import shutil
from pathlib import Path

import arrow
from django.conf import settings
from django.core.management.base import BaseCommand

from main.utils import get_time_from_file_stem


class Command(BaseCommand):
    help = 'remove useless images from cctv_detected folder'

    def handle(self, *args, **options):
        image_detected_dir = settings.BASE_DIR / 'media' / 'cctv_detected'
        now  = arrow.now()
        for image_path in image_detected_dir.glob('*.jpg'):
            # check if the file is older than 5 hours
            if now - get_time_from_file_stem(image_path.stem) > arrow.timedelta(hours=5):
                image_path.unlink()
