from django.test import TestCase
from .models import Campground
from django.urls import reverse

# Create your tests here.
def createCampground(name, imageUrl):
    return Campground.objects.create(name=name, imageUrl=imageUrl)

class CampgroundViewTest(TestCase):
    def test_no_Campground(self):
        response = self.client.get(reverse('yelpCamp:campgrounds'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['campgroundList'], [])


    def test_two_Campground(self):
        createCampground(name='camp 1', imageUrl='http://www.nextcampsite.com/wp-content/uploads/2014/07/Lost-Creek-Campground-D08.jpg')
        createCampground(name='camp 2', imageUrl='http://www.nextcampsite.com/wp-content/uploads/2014/07/Lost-Creek-Campground-D08.jpg')
        response = self.client.get(reverse('yelpCamp:campgrounds'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['campgroundList'], ['<Campground: camp 2>', '<Campground: camp 1>'])

