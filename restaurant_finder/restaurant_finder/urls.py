"""restaurant_finder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from restaurants.views import RestaurantList, RestaurantDetail
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pwa.urls')),  # Include PWA URLs
    path('', include('restaurants.urls')),
    path('api/restaurants/', RestaurantList.as_view(), name='restaurant-list'),  # For listing and adding restaurants
    path('api/restaurants/<int:pk>/', RestaurantDetail.as_view(), name='restaurant-detail'),  # For retrieving, updating, or deleting a single restaurant

    path('login/', auth_views.LoginView.as_view(), name='login'),  # Login URL
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout URL
]

