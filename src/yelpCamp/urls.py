from django.urls import path

from . import views

app_name = 'yelpCamp'
urlpatterns = [
    path('', views.landing, name='landing'),
    path('campgrounds/', views.campgrounds, name='campgrounds'),
    path('campgrounds/new', views.campgroundsNew, name='campgroundsNew'),
    path('campgrounds/<int:campground_id>', views.campgroundDetails, name='campgroundDetails'),
    path('campgrounds/<int:campground_id>/edit', views.campgroundEdit, name='campgroundEdit'),
    path('campgrounds/<int:campground_id>/comments/new', views.commentsNew, name='commentsNew'),
    path('campgrounds/<int:campground_id>/comments', views.comments, name='comments'),
    path('signup', views.userSignup, name='userSignup'),
]
