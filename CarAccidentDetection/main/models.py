from django.db import models
from django.contrib.auth.models import User

# TODO: add virifier.

class PoliceOfficer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    badge_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.user.username


class Accident(models.Model):
    # accident info
    location = models.CharField(max_length=255)

    # about CV model
    detected_time = models.DateTimeField()
    confidence = models.FloatField(null=True, blank=True)  # model confidence

    # images
    video_frame_folder = models.CharField(max_length=255)  # video is image frames, this is the folder name
    key_frame = models.CharField(max_length=255)  # key frame image

    # manual verification
    is_verified = models.BooleanField(default=False, blank=True)
    verifier = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='accidents',
        null=True,
    )  # who verified the accident
    verified_time = models.DateTimeField(null=True)

    # dispatched police
    dispatched_time = models.DateTimeField(null=True, blank=True)
    dispatched_police = models.ForeignKey(
        PoliceOfficer,
        on_delete=models.CASCADE,
        related_name='dispatched_accidents',
        null=True,
    )

    def __str__(self):
        return f"{self.location} on {self.detected_time.strftime('%Y-%m-%d %H:%M:%S')}"


class AccidentReport(models.Model):
    SCENE_DIAGRAME_FILENAME = 'scene_diagram.png'
    accident = models.OneToOneField(Accident, on_delete=models.CASCADE, related_name='report')
    scene_diagram = models.ImageField(upload_to='cctv_accident/', null=True, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.accident.id}"


class CCTV(models.Model):
    cctv_id = models.CharField(max_length=50, unique=True)
    road_section = models.CharField(max_length=255)
    px = models.FloatField()
    py = models.FloatField()
    site_url = models.URLField()
    status = models.CharField(max_length=50)
    agency_codes = models.CharField(max_length=50)
    local_call_service = models.CharField(max_length=50)
    extension = models.CharField(max_length=50)
    county_code = models.CharField(max_length=50)
    area_code = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=50)
    hotspot = models.BooleanField(default=False)  # 是否為熱點區域
    mjpeg_url = models.URLField(null=True, blank=True)  # MJPEG URL for the CCTV stream

    def __str__(self):
        return self.road_name
