from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django.core.management import call_command


scheduler = BackgroundScheduler()


def start():
    scheduler.add_job(
        detect_accident,
        trigger=IntervalTrigger(seconds=30),
        id="detect_accident",
        name="每 5 秒偵測車禍",
        replace_existing=True,
    )
    scheduler.add_job(
        remove_useless_images,
        trigger=IntervalTrigger(hours=1),
        id="remove_useless_images",
        name="每 1 小時刪除無用圖片",
        replace_existing=True,
    )
    scheduler.start()

def detect_accident():
    call_command("detect_accident")

def remove_useless_images():
    call_command("remove_useless_images")
