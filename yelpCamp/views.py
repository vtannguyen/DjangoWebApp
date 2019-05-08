from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.utils import timezone
import json
from django.views import generic
from django.http import QueryDict
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Campground, Comment
from .forms import NewCampgroundForm, NewCommentForm, SignUpForm
from django.contrib.auth.forms import UserCreationForm


def landing(request):
    return render(request, 'yelpCamp/landing.html')


def campgrounds(request):
    if request.method == 'POST' and request.user.is_authenticated:
        form = NewCampgroundForm(request.POST)
        if form.is_valid():
            campground_instance = Campground(
                name=form.cleaned_data['name'],
                imageUrl=form.cleaned_data['imageUrl'],
                description=form.cleaned_data['description'],
                price=form.cleaned_data['price'],
                user=request.user
            )
            campground_instance.save()

            return HttpResponseRedirect(reverse('yelpCamp:campgrounds'))
        else:
            return render(request, 'yelpCamp/campgroundsNew.html', {'form': form})
    else:
        campgroundList = Campground.objects.all().order_by('-name')
        return render(request, 'yelpCamp/campgrounds.html', {'campgroundList': campgroundList})


@login_required
def campgroundsNew(request):
    form = NewCampgroundForm(initial={'name': '', 'imageUrl': ''})
    context = {'form': form}
    return render(request, 'yelpCamp/campgroundsNew.html', context)


def campgroundDetails(request, campground_id):
    campground = get_object_or_404(Campground, pk=campground_id)
    comments = Comment.objects.filter(campground__id__exact=campground_id)

    if request.method == 'POST':
        if request.user.is_authenticated and campground.user == request.user:
            form = NewCampgroundForm(request.POST)
            if form.is_valid():
                campground.name = form.cleaned_data['name']
                campground.description = form.cleaned_data['description']
                campground.imageUrl = form.cleaned_data['imageUrl']
                campground.price = form.cleaned_data['price']
                campground.save()
    elif request.method == 'DELETE':
        if request.user.is_authenticated and campground.user == request.user:
            campground.delete()
        return HttpResponseRedirect(reverse('yelpCamp:campgrounds'))

    context = {
        'campground': campground,
        'comments': comments
    }
    return render(request, 'yelpCamp/campgroundDetails.html', context)


@login_required
def campgroundEdit(request, campground_id):
    campground = get_object_or_404(Campground, pk=campground_id)
    form = NewCampgroundForm(initial={
        'name': campground.name,
        'imageUrl': campground.imageUrl,
        'description': campground.description,
        'price': campground.price
    })
    if campground.user.username == request.user.username:
        return render(request, 'yelpCamp/campgroundEdit.html', {
            'form': form,
            'campground_id': campground_id
        })
    else:
        return HttpResponseRedirect(reverse('yelpCamp:campgroundDetails', args=(campground_id,)))


@login_required
def commentsNew(request, campground_id):
    form = NewCommentForm(initial={'text': ''})
    campgroundName = Campground.objects.get(pk=campground_id).name
    contex = {'form': form, 'campground_id': campground_id, 'campgroundName': campgroundName}
    return render(request, 'yelpCamp/commentsNew.html', contex)


def comments(request, campground_id):
    if request.method == 'POST' and request.user.is_authenticated:
        form = NewCommentForm(request.POST)
        if form.is_valid():
            campground_instance = Campground.objects.get(pk=campground_id)
            comment_instance = Comment(
                text=form.cleaned_data['text'],
                timestamp=timezone.now(),
                campground=campground_instance,
                user=request.user
            )
            comment_instance.save()

            url = reverse('yelpCamp:campgroundDetails', args=(campground_id,))

            return HttpResponseRedirect(url)
        else:
            return render(request, 'yelpCamp/campgroundsNew.html', {'form': form})
    else:
        redirectUrl = reverse('yelpCamp:campgroundDetails', args=(campground_id,))
        return HttpResponseRedirect(redirectUrl)


def userSignup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('yelpCamp:campgrounds'))
        else:
            return render(request, 'yelpCamp/userSignup.html', {'form': form})
    elif request.method == 'GET':
        context = {
            'form': SignUpForm
        }
        return render(request, 'yelpCamp/userSignup.html', context)
