from django.db import models
from django.contrib.auth.models import User


class Map(models.Model):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="maps/logos/", null=True, blank=True)

    def __str__(self):
        return self.name


class Floor(models.Model):
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    floor_number = models.IntegerField()
    floor_map = models.FileField(upload_to="floors/maps/")

    def __str__(self):
        return f"{self.map.name} - Floor {self.floor_number} {self.id}"


class PlaceType(models.Model):
    type_name = models.CharField(max_length=100)


class Place(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    place_type = models.ForeignKey(
        PlaceType, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to="places/logos/", null=True, blank=True)
    working_hours = models.CharField(max_length=100, null=True, blank=True)
    svg_path_data = models.TextField()

    def __str__(self):
        return self.name
