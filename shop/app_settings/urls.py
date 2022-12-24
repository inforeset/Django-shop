from django.urls import path

from .api import SettingsView

urlpatterns = [
    path('settings/', SettingsView.as_view(), name='authors'),
]