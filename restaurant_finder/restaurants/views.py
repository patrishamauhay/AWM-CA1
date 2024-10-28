from django.shortcuts import render
from .models import Restaurant
from django.db.models import Q

def map_view(request):
    # Initialize the search variable
    search_input = request.GET.get('search', '')

    # Filter restaurants based on the search input (if provided)
    if search_input:
        restaurants = list(Restaurant.objects.filter(name__icontains=search_input).values('name', 'address', 'latitude', 'longitude'))
    else:
        restaurants = list(Restaurant.objects.values('name', 'address', 'latitude', 'longitude'))

    # Set a default location for the map center, or use the first restaurant's location if available
    initial_location = restaurants[0] if restaurants else {'latitude': 0, 'longitude': 0}

    return render(request, 'index.html', {
        'restaurants': restaurants,
        'initial_location': initial_location,
        'search_input': search_input  # Pass search input to the template
    })
