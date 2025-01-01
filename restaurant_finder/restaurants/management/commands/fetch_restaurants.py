# restaurants/management/commands/fetch_restaurants.py
import requests
from django.core.management.base import BaseCommand
from restaurants.models import Restaurant

class Command(BaseCommand):
    help = 'Fetch restaurant data from OpenStreetMap Overpass API and store it in the database'

    def handle(self, *args, **kwargs):
        # Specify the location (latitude, longitude) for the search area
        location = '40.7128,-74.0060'  # Example: New York City (replace with your desired coordinates)
        radius = 5000  # Search radius in meters (5km radius around the location)

        # Define Overpass API query to search for restaurants
        query = f"""
        [out:json];
        (
          node["amenity"="restaurant"](around:{radius},{location});
          way["amenity"="restaurant"](around:{radius},{location});
          relation["amenity"="restaurant"](around:{radius},{location});
        );
        out body;
        """

        # Send request to Overpass API
        url = "https://overpass-api.de/api/interpreter?data=" + query
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            for element in data.get('elements', []):
                # Extract relevant restaurant data
                if 'tags' in element:
                    name = element['tags'].get('name')
                    address = element['tags'].get('addr:full')  # Example address field
                    latitude = element.get('lat')
                    longitude = element.get('lon')

                    # Only add restaurants with valid data
                    if name and latitude and longitude:
                        # Check if restaurant already exists, to avoid duplicates
                        restaurant, created = Restaurant.objects.get_or_create(
                            name=name,
                            latitude=latitude,
                            longitude=longitude,
                            defaults={'address': address},
                        )
                        if created:
                            self.stdout.write(self.style.SUCCESS(f'Successfully added restaurant: {name}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Invalid restaurant data for {name}'))

            self.stdout.write(self.style.SUCCESS('Completed fetching and saving restaurant data.'))

        else:
            self.stdout.write(self.style.ERROR('Failed to fetch data from Overpass API'))

