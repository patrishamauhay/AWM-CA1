from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.db import models
from django.contrib.auth.models import User

# Defining Restaurants model
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True, null=True)  # Allow null and blank addresses
    description = models.TextField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = gis_models.PointField(geography=True, blank=True, null=True)
    rating = models.FloatField(default=0) 

class WorldBorder(models.Model):

    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.

    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2, null=True)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = models.MultiPolygonField()

    def __str__(self):
        return self.name

    # Add a Many-to-Many relationship to store favorite restaurants
    User.add_to_class(
        'favorite_restaurants', 
        models.ManyToManyField(Restaurant, related_name='favorited_by')
    )





