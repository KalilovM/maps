from django.db import models
from django.contrib.auth.models import User


class Map(models.Model):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="maps/logos/", null=True, blank=True)

    def __str__(self):
        return self.name


class Floor(models.Model):
    map = models.ForeignKey(Map, on_delete=models.CASCADE, related_name="floors")
    floor_number = models.IntegerField()
    floor_map = models.FileField(upload_to="floors/maps/")

    @classmethod
    def get_floor_with_places(cls, floor_id):
        return cls.objects.prefetch_related("places").get(id=floor_id)

    def places_as_list(self):
        return list(
            self.places.values(
                "id", "name", "description", "svg_path_data", "logo", "working_hours"
            )
        )

    def get_svg_content(self):
        if self.floor_map:
            with open(self.floor_map.path, "r") as svg_file:
                return svg_file.read()
        return ""

    def __str__(self):
        return f"{self.map.name} - Floor {self.floor_number} {self.id}"


class PlaceType(models.Model):
    type_name = models.CharField(max_length=100)


class Place(models.Model):
    floor = models.ForeignKey(Floor, related_name="places", on_delete=models.CASCADE)
    place_type = models.ForeignKey(
        PlaceType, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to="places/logos/", null=True, blank=True)
    working_hours = models.CharField(max_length=100, null=True, blank=True)
    svg_path_data = models.TextField()

    @classmethod
    def create_place(cls, floor_instance, path_data):
        """
        Creates a Place instance from SVG path data.
        :param floor_instance: Floor instance the place belongs to
        :param path_data: Dictionary containing the 'd' attribute and potentially other data
        :return: Place instance (created and saved)
        """
        place_name = path_data.get("name", "Unnamed Place")
        svg_path_data = path_data.get("d", "")
        return cls.objects.create(
            floor=floor_instance,
            name=place_name,
            svg_path_data=svg_path_data,
        )

    def __str__(self):
        return self.name
