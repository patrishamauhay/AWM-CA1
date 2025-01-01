# This will make te model data available via a REST API

from rest_framework import serializers
from .models import Restaurant, WorldBorder
from django.contrib.gis.geos import Point


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'address', 'description', 'latitude', 'longitude', 'location')
        extra_kwargs = {'location': {'read_only': True}}  # Location will be auto-populated


class WorldBorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorldBorder
        fields = ('id', 'name', 'area', 'pop2005', 'fips', 'iso2', 'iso3', 'un', 'region', 'subregion', 'lon', 'lat', 'mpoly')
