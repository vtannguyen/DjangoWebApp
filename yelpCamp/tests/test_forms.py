from django.test import TestCase
from ..forms import NewCampgroundForm

CORRECT_IMAGE_URL = 'http://www.nextcampsite.com/wp-content/uploads/2014/07/Lost-Creek-Campground-D08.jpg'

class NewCampgroundFormTest(TestCase):
    def test_new_campground_form_valid(self):
        form_data = {
            'name': 'camp 1',
            'imageUrl': CORRECT_IMAGE_URL,
            'description': 'This campground is beautiful'
        }
        form = NewCampgroundForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_new_campground_form_noname(self):
        form_data_noname = {'name': '', 'imageUrl': CORRECT_IMAGE_URL}
        form = NewCampgroundForm(data=form_data_noname)
        self.assertFalse(form.is_valid())

    def test_new_campground_form_noimage(self):
        form_data_noimage = {'name': 'camp 1', 'imageUrl': ''}
        form = NewCampgroundForm(data=form_data_noimage)
        self.assertFalse(form.is_valid())

    def test_new_campground_form_wrongUrl(self):
        form_data_wrongUrl = {'name': 'camp 1', 'imageUrl': 'fasdfasdfasdfafds'}
        form = NewCampgroundForm(data=form_data_wrongUrl)
        self.assertFalse(form.is_valid())

    def test_new_campground_from_noDescription(self):
        form_data_noDescription = {'name': 'camp 1', 'imageUrl': CORRECT_IMAGE_URL, 'description': ''}
        form = NewCampgroundForm(data=form_data_noDescription)
        self.assertFalse(form.is_valid())

