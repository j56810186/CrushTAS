import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Run external CCTV (MJPEG frame) fetcher'

    def handle(self, *args, **options):
        import arrow
        start = arrow.now()
        script_path = settings.BASE_DIR / 'cctv_fetcher' / 'main.py'  # 修改成你的實際路徑
        subprocess.run(['python', str(script_path)])
        end = arrow.now()
        print(f"Time taken: {end - start}")
