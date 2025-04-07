# urls.py
from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import (
    UserLoginView,
    IndexRedirectView,
    AccidentListView,
    AccidentDetailView,
    AccidentVerifyView,
    AccidentReportGenerateView,
    AccidentReportListView,
    AccidentReportDetailView,
)

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('accidents/', AccidentListView.as_view(), name='accident_list'),
    path('accidents/<int:pk>/', AccidentDetailView.as_view(), name='accident_detail'),
    path('accidents/<int:pk>/verify/', AccidentVerifyView.as_view(), name='accident_verify'),
    path('accidents/<int:pk>/report/generate', AccidentReportGenerateView.as_view(), name='accident_report_generate'),
    path('accidents/reports/', AccidentReportListView.as_view(), name='accident_report_list'),
    path('accidents/reports/<int:pk>/', AccidentReportDetailView.as_view(), name='accident_report_detail'),
    path('', IndexRedirectView.as_view(), name='index_redirect'),
]
