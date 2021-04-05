from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('home/', views.home, name="user_profile"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)