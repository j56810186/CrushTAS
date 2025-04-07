import arrow
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import DetailView, ListView, RedirectView
from django.views.generic.edit import UpdateView

from .models import Accident, AccidentReport, PoliceOfficer


class UserLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


class IndexRedirectView(RedirectView, LoginRequiredMixin):
    pattern_name = 'accident_list'
    permanent = False


class AccidentListView(LoginRequiredMixin, ListView):
    model = Accident
    template_name = 'accident_list.html'
    context_object_name = 'accidents'
    ordering = ['-detected_time']

    def get_queryset(self):
        queryset = super().get_queryset()
        is_verified = self.request.GET.get('verified', None)
        if is_verified in ('0', '1'):
            if is_verified == '1':
                is_verified = True
            else:  # is_verified == '0'
                is_verified = False
            queryset = queryset.filter(is_verified=is_verified)
        return queryset


class AccidentDetailView(LoginRequiredMixin, DetailView):
    model = Accident
    template_name = 'accident_detail.html'
    context_object_name = 'accident'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = []
        for path in (settings.BASE_DIR / self.object.video_frame_folder.lstrip('/')).iterdir():
            if path.is_file() and path.name != AccidentReport.SCENE_DIAGRAME_FILENAME:
                context['images'].append(path.name)
        context['images'].sort(key=lambda x: x.split('/')[-1])
        context['police_officers'] = PoliceOfficer.objects.all()
        return context


class AccidentVerifyView(LoginRequiredMixin, UpdateView):
    model = Accident
    fields = ['is_verified', 'dispatched_police', 'dispatched_time']

    def form_valid(self, form):
        if form.cleaned_data.get('is_verified') and self.object.verified_time is None:
            self.object.verifier = self.request.user
            self.object.verified_time = arrow.now().datetime
            self.object.dispatched_time = arrow.now().datetime
        self.object.save()

        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": True})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
        return super().form_invalid(form)


class AccidentReportGenerateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        accident = get_object_or_404(Accident, pk=kwargs['pk'])

        # FIXME: generate scene diagram and save it here
        scene_diagram = accident.video_frame_folder + '/' + AccidentReport.SCENE_DIAGRAME_FILENAME

        AccidentReport.objects.update_or_create(
            accident=accident,
            defaults={'scene_diagram': scene_diagram}
        )
        return JsonResponse({'success': True})


class AccidentReportListView(LoginRequiredMixin, ListView):
    model = AccidentReport
    template_name = 'accident_report_list.html'
    context_object_name = 'accident_reports'
    ordering = ['-generated_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        location = self.request.GET.get('location', None)
        if location:
            queryset = queryset.filter(accident__location__icontains=location)
        return queryset


class AccidentReportDetailView(LoginRequiredMixin, DetailView):
    model = AccidentReport
    template_name = 'accident_report_detail.html'
    context_object_name = 'report'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = []
        for path in (settings.BASE_DIR / self.object.accident.video_frame_folder.lstrip('/')).iterdir():
            if path.is_file() and path.name != AccidentReport.SCENE_DIAGRAME_FILENAME:
                context['images'].append(path.name)
        context['images'].sort(key=lambda x: x.split('/')[-1])
        return context
