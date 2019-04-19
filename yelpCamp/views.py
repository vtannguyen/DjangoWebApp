from django.shortcuts import render
from django.views import generic

# Create your views here.
from django.http import HttpResponse
from .models import Campground

def landing(request):
    return render(request, 'yelpCamp/landing.html')

class CampgroundView(generic.ListView):
    template_name = 'yelpCamp/campgrounds.html'
    context_object_name = 'campgroundList'

    def get_queryset(self):
        return Campground.objects.all().order_by('-name')
