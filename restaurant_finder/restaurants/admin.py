from django.contrib import admin
from .models import Restaurant
from .models import WorldBorder


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'description', 'latitude', 'longitude')

admin.site.register(WorldBorder, admin.ModelAdmin)


