from django.shortcuts import render
from .models import Restaurant

def map_view(request):
    # Get all restaurants and format data for JSON output
    restaurants = list(Restaurant.objects.values('name', 'address', 'latitude', 'longitude'))
    
    # Set a default location for the map center, or use the first restaurant's location if available
    initial_location = restaurants[0] if restaurants else {'latitude': 0, 'longitude': 0}

    return render(request, 'restaurant_list.html', {
        'restaurants': restaurants,
        'initial_location': initial_location,
    })
