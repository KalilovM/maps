from django.urls import path

# media url
from django.conf import settings
from django.conf.urls.static import static

from .views import upload_floor_svg, success, map_view

urlpatterns = [
    path("upload/", upload_floor_svg, name="upload_floor_svg"),
    path("success/", success, name="success"),
    path("map/<int:floor_id>/", map_view, name="map_view"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
