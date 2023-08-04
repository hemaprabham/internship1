from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings

from .views import UrineStripColorAPIView

urlpatterns = [
    path('', UrineStripColorAPIView.as_view(), name='urine_strip_api'),
]
