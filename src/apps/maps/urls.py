from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import FloorViews

urlpatterns = [
    path("upload/", FloorViews.upload_floor_svg, name="upload_floor_svg"),
    path("success/", FloorViews.success, name="success"),
    path("map/<int:floor_id>/", FloorViews.map_view, name="map_view"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
