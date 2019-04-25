from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Campground, Comment
from .forms import NewCampgroundForm, NewCommentForm


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
            return HttpResponseRedirect(reverse('yelpCamp:campgroundsNew'))

    else:
        campgroundList = Campground.objects.all().order_by('-name')
        return render(request, 'yelpCamp/campgrounds.html', {'campgroundList': campgroundList})


def campgroundsNew(request):
    form = NewCampgroundForm(initial={'name': '', 'imageUrl': ''})
    context = {'form': form}
    return render(request, 'yelpCamp/campgroundsNew.html', context)


def campgroundDetails(request, campground_id):
    campground = get_object_or_404(Campground, pk=campground_id)
    comments = Comment.objects.filter(campground__id__exact=campground_id)
    context = {
        'campground': campground,
        'comments': comments
    }
    return render(request, 'yelpCamp/campgroundDetails.html', context)


def commentsNew(request, campground_id):
    form = NewCommentForm(initial={'text': ''})
    contex = {'form': form, 'campground_id': campground_id}
    return render(request, 'yelpCamp/commentsNew.html', contex)


def comments(request, campground_id):
    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            campground_instance = Campground.objects.get(pk=campground_id)
            comment_instance = Comment(
                text=form.cleaned_data['text'],
                timestamp=timezone.now(),
                campground=campground_instance)
            comment_instance.save()

            url = reverse('yelpCamp:campgroundDetails', args=(campground_id,))

            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect(reverse('yelpCamp:campgroundsNew'))
    elif request.method == 'GET':
        redirectUrl = reverse('yelpCamp:campgroundDetails', args=(campground_id,))
        return HttpResponseRedirect(redirectUrl)

