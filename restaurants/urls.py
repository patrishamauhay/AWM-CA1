from django.urls import path
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.map_view, name='index'),
    path('add-to-favorites/<int:restaurant_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/', views.view_favorites, name='favorites'),
    
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
