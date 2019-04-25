from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Campground
from .forms import NewCampgroundForm


def landing(request):
    return render(request, 'yelpCamp/landing.html')


def campgrounds(request):
    if request.method == 'POST':
        form = NewCampgroundForm(request.POST)
        if form.is_valid():
            campground_instance = Campground(
                name=form.cleaned_data['name'],
                imageUrl=form.cleaned_data['imageUrl'],
                description=form.cleaned_data['description']
            )
            campground_instance.save()

            return HttpResponseRedirect(reverse('yelpCamp:campgrounds'))
    else:
        campgroundList = Campground.objects.all().order_by('-name')
        return render(request, 'yelpCamp/campgrounds.html', {'campgroundList': campgroundList})


def campgroundsNew(request):
    form = NewCampgroundForm(initial={'name': '', 'imageUrl': ''})
    context = {'form': form}
    return render(request, 'yelpCamp/campgroundsNew.html', context)


def campgroundDetails(request, campground_id):
    campground = get_object_or_404(Campground, pk=campground_id)
    return render(request, 'yelpCamp/campgroundDetails.html', {'campground': campground})
