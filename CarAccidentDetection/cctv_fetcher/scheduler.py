from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django.core.management import call_command


scheduler = BackgroundScheduler()


def start():
    scheduler.add_job(
        fetch_frames_job,
        trigger=IntervalTrigger(seconds=30),
        id="fetch_cctv_job",
        name="每 30 秒抓取一次 MJPEG 圖片",
        replace_existing=True,
    )
    scheduler.start()

def fetch_frames_job():
    call_command("fetch_cctv")
