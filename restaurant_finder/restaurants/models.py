from django.db import models
from django.contrib.gis.db import models as gis_models

# Defining Restaurants model
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = gis_models.PointField(geography=True, blank=True, null=True)

    def __str__(self):
        return self.name



