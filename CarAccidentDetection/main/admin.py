from django.contrib import admin
from .models import Accident, AccidentReport, PoliceOfficer


@admin.register(PoliceOfficer)
class PoliceOfficerAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Accident)
class AccidentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'location', 'detected_time', 'confidence',
        'is_verified', 'verifier', 'verified_time',
        'dispatched_police', 'dispatched_time'
    )
    list_filter = ('is_verified', 'verifier', 'dispatched_police')
    search_fields = ('location', 'video_frame_folder', 'key_frame')
    autocomplete_fields = ('verifier', 'dispatched_police')  # 方便選人
    readonly_fields = ('verified_time',)  # 若要讓時間由系統控制，可鎖定不編輯
    ordering = ('-detected_time',)


@admin.register(AccidentReport)
class AccidentReportAdmin(admin.ModelAdmin):
    list_display = ('accident', 'generated_at')
    search_fields = ('accident__location', 'summary')
    readonly_fields = ('generated_at',)
