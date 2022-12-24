from app_settings.models import SiteSettings

from app_settings.serializer import SiteSettingsSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin


class SettingsView(ListModelMixin, GenericAPIView):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer

    def get(self, request):
        return self.list(request)