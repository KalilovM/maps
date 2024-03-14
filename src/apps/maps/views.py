from django.shortcuts import render, redirect
from .models import Place, Floor
from .forms import FloorForm
from utils.parse_svg import parse_svg, add_ids_to_svg
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def upload_floor_svg(request):
    if request.method == "POST":
        form = FloorForm(request.POST, request.FILES)
        if form.is_valid():
            floor_instance = form.save()
            add_ids_to_svg(floor_instance.floor_map.path)
            svg_paths = parse_svg(floor_instance.floor_map.path)
            for path_data in svg_paths:
                Place.objects.create(
                    floor=floor_instance,
                    svg_path_data=path_data["d"],
                    name=path_data["name"],
                )
            return redirect("success")  # Adjust as needed
    else:
        form = FloorForm()
    return render(request, "upload_floor_svg.html", {"form": form})


def success(request):
    return render(request, "success.html")


def map_view(request, floor_id):
    floor = Floor.objects.get(id=floor_id)
    places = Place.objects.filter(floor=floor).values(
        "id", "name", "description", "svg_path_data", "logo", "working_hours"
    )
    svg_content = ""
    if floor.floor_map:
        with open(floor.floor_map.path, "r") as file:
            svg_content = file.read()
    return render(
        request,
        "show_svg.html",
        {
            "floor": floor,
            "places": list(places),
            "svg_content": svg_content,
            "MEDIA_URL": settings.MEDIA_URL,
        },
    )
