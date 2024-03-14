from django.shortcuts import render, redirect
from django.conf import settings
from .models import Place, Floor
from .forms import FloorForm
from utils.svg_handler import (
    SVGHandler,
)
import logging

logger = logging.getLogger(__name__)


class FloorViews:
    @staticmethod
    def upload_floor_svg(request):
        if request.method == "POST":
            form = FloorForm(request.POST, request.FILES)
            if form.is_valid():
                floor_instance = form.save()
                svg_path = floor_instance.floor_map.path

                SVGHandler.add_ids_to_svg(svg_path)
                svg_paths = SVGHandler.parse_svg(svg_path)
                for path in svg_paths:
                    Place.create_place(floor_instance, path)
                return redirect("success")
        else:
            form = FloorForm()
        return render(request, "upload_floor_svg.html", {"form": form})

    @staticmethod
    def success(request):
        return render(request, "success.html")

    @staticmethod
    def map_view(request, floor_id):
        floor = Floor.get_floor_with_places(floor_id)
        places = floor.places_as_list()
        svg_content = floor.get_svg_content()

        return render(
            request,
            "show_svg.html",
            {
                "floor": floor,
                "places": places,
                "svg_content": svg_content,
                "MEDIA_URL": settings.MEDIA_URL,
            },
        )
