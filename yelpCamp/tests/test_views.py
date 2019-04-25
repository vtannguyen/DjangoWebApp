from django.test import TestCase
from ..models import Campground
from django.urls import reverse
from ..forms import NewCampgroundForm

# Create your tests here.
CORRECT_IMAGE_URL = 'http://www.nextcampsite.com/wp-content/uploads/2014/07/Lost-Creek-Campground-D08.jpg'
def createCampground(name, imageUrl):
    return Campground.objects.create(name=name, imageUrl=imageUrl)

class CampgroundViewTest(TestCase):
    def test_no_Campground(self):
        response = self.client.get(reverse('yelpCamp:campgrounds'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['campgroundList'], [])

    def test_two_Campground(self):
        createCampground(name='camp 1', imageUrl=CORRECT_IMAGE_URL)
        createCampground(name='camp 2', imageUrl=CORRECT_IMAGE_URL)
        response = self.client.get(reverse('yelpCamp:campgrounds'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['campgroundList'], ['<Campground: camp 2>', '<Campground: camp 1>'])

    def test_open_campground_create_form(self):
        response = self.client.get(reverse('yelpCamp:campgroundsNew'))
        self.assertEqual(response.status_code, 200)

    def test_create_new_campground(self):
        response = self.client.post(reverse(
            'yelpCamp:campgrounds'),
            {'name': 'test Camp', 'imageUrl': CORRECT_IMAGE_URL, 'description': 'this is awesome'})

        camp_test = Campground.objects.get(name='test Camp')
        self.assertRedirects(response, reverse('yelpCamp:campgrounds'), status_code=302, target_status_code=200)
        self.assertEqual(camp_test.imageUrl, CORRECT_IMAGE_URL)
        self.assertEqual(camp_test.description, 'this is awesome')


class CampgroundDetailsViewTest(TestCase):
    def test_incorrect_campground_id(self):
        url = reverse('yelpCamp:campgroundDetails', args=(5,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_correct_campground_id(self):
        camp_test = createCampground(name='camp 1', imageUrl=CORRECT_IMAGE_URL)
        url = reverse('yelpCamp:campgroundDetails', args=(camp_test.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, camp_test.name)
        self.assertContains(response, camp_test.imageUrl)
        self.assertContains(response, camp_test.description)


