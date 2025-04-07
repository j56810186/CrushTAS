import shutil
from pathlib import Path

import arrow
from django.conf import settings
from django.core.management.base import BaseCommand

from main.cv_model import ModelRegistry
from main.models import Accident, CCTV
from main.utils import get_frame_stems_in_range


class Command(BaseCommand):
    help = 'detect car accident'

    def handle(self, *args, **options):
        cctv_dict = {}
        for cctv in CCTV.objects.all():
            if cctv.hotspot:
                mjpeg_url = cctv.mjpeg_url
                cctv_dict[mjpeg_url.split('/')[-1]] = cctv

        image_source_dir = settings.BASE_DIR / 'media' / 'cctv'
        image_detecting_dir = settings.BASE_DIR / 'media' / 'cctv_detecting'
        image_detected_dir = settings.BASE_DIR / 'media' / 'cctv_detected'
        image_accident_dir = settings.BASE_DIR / 'media' / 'cctv_accident'

        # move all images from media/cctv to media/cctv_detecting, to prevent duplicate detection
        source_files = list(image_source_dir.glob('**/*.jpg'))
        shutil.copytree(image_source_dir, image_detecting_dir, dirs_exist_ok=True)
        for file in source_files:
            file.unlink()

        # detect car accident
        results = []
        image_paths_list = [[]]
        model = ModelRegistry.get_model()
        for dir in image_detecting_dir.iterdir():
            if dir.is_dir():
                for image_path in dir.iterdir():
                    if image_path.is_file():
                        if len(image_paths_list[-1]) >= 64:
                            image_paths_list.append([])
                        image_paths_list[-1].append(image_path)
        for image_paths in image_paths_list:
            if image_paths:
                results.extend(model.predict(image_paths, verbose=False))

        # move all images from media/cctv_detecting to media/cctv_detected
        if not image_detected_dir.exists():
            shutil.copytree(image_detecting_dir, image_detected_dir, dirs_exist_ok=True)
        else:
            for dir in image_detecting_dir.iterdir():
                if dir.is_dir():
                    for image_path in dir.iterdir():
                        if image_path.is_file():
                            shutil.move(image_path, image_detected_dir / dir.name / image_path.name)

        # create accident by results
        results.sort(key=lambda x: x.path)  # sort by time
        accident = None
        for result in results:
            if len(result.boxes) > 0 and result.boxes[0].cls == 0:
                # create accident
                cctv = cctv_dict[result.path.split('/')[-2]]
                accident = Accident.objects.create(
                    location=cctv.road_section,
                    key_frame=result.path,
                    detected_time=arrow.now().datetime,
                    confidence=result.boxes[0].conf,
                )
                break

        # TODO: Handle multiple accident happen at the same time.

        if accident is None:
            return

        if not image_accident_dir.exists():
            image_accident_dir.mkdir()

        target_dir = image_accident_dir / f"{cctv.cctv_id}_{arrow.get(accident.detected_time).format('YYYYMMDD_HHmmss')}"
        key_frame_path = Path(accident.key_frame)
        for stem in get_frame_stems_in_range(key_frame_path.stem):
            file_path = key_frame_path.parent / f"{stem}.jpg"
            if not target_dir.exists():
                target_dir.mkdir(parents=True)
            if file_path.exists():
                shutil.move(file_path, target_dir / f"{stem}.jpg")
        accident.video_frame_folder = f'/media/cctv_accident/{target_dir.name}'
        accident.key_frame = f"{accident.video_frame_folder}/{key_frame_path.stem}.jpg"
        accident.save()
