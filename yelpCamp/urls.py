from django.urls import path

from . import views

app_name = 'yelpCamp'
urlpatterns = [
    path('', views.landing, name='landing'),
    path('campgrounds/', views.campgrounds, name='campgrounds'),
    path('campgrounds/new', views.campgroundsNew, name='campgroundsNew'),
]
