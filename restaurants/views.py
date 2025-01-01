import random
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Restaurant
from django.contrib.auth.views import LoginView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RestaurantSerializer

@login_required
def add_to_favorites(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    
    # Check if the restaurant is already in the user's favorites
    if restaurant in request.user.favorite_restaurants.all():
        # Remove from favorites
        request.user.favorite_restaurants.remove(restaurant)
    else:
        # Add to favorites
        request.user.favorite_restaurants.add(restaurant)
    
    # Redirect to the page where the user was
    return redirect(request.META.get('HTTP_REFERER', 'restaurant-list'))
 

@login_required
def view_favorites(request):
    favorites = request.user.favorite_restaurants.all()
    return render(request, 'favorites.html', {'favorites': favorites})


def home(request):
    """
    Home view: Redirect users based on their role or show the homepage for unauthenticated users.
    """
    if request.user.is_authenticated:
        if request.user.is_superuser:  # Check if the user is an admin
            return redirect('/admin/')  # Redirect to the admin panel
        else:
            return redirect('map_view')  # Redirect regular users to the map view
    return render(request, 'home.html')  # Render the homepage for unauthenticated users

@login_required
def map_view(request):
    """
    Map view: Display a searchable map with restaurants.
    Requires the user to be logged in.
    """
    # Initialize the search variable
    search_input = request.GET.get('search', '')

    # Filter restaurants based on the search input (if provided)
    if search_input:
        restaurants = Restaurant.objects.filter(name__icontains=search_input)
    else:
        restaurants = Restaurant.objects.all()

    # Set a default location for the map center, or use the first restaurant's location if available
    initial_location = restaurants.first()  # Use .first() to avoid IndexError when there are no restaurants
    initial_location = initial_location if initial_location else {'latitude': 0, 'longitude': 0}

     # Generate random ratings between 1 and 5
    random_ratings = {restaurant.id: random.randint(1, 5) for restaurant in restaurants}

    return render(request, 'index.html', {
        'restaurants': restaurants,
        'initial_location': initial_location,
        'search_input': search_input,
        'random_ratings': random_ratings

    })

class CustomLoginView(LoginView):
    def get_success_url(self):
        if self.request.user.is_superuser:
            return '/admin/'  # Redirect to admin panel if the user is an admin
        return '/'  # Redirect to the homepage or restaurant map for regular users


class RestaurantList(APIView):
    """
    List all restaurants or create a new restaurant.
    """
    def get(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RestaurantDetail(APIView):
    """
    Retrieve, update or delete a restaurant instance.
    """
    def get_object(self, pk):
        try:
            return Restaurant.objects.get(pk=pk)
        except Restaurant.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        restaurant = self.get_object(pk)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data)

    def put(self, request, pk):
        restaurant = self.get_object(pk)
        serializer = RestaurantSerializer(restaurant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        restaurant = self.get_object(pk)
        restaurant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    