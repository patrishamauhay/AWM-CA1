from django.urls import path
from django.contrib import admin
from . import views


urlpatterns = [
    path('', views.map_view, name='index'),

]
