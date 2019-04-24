from django.test import TestCase
from ..forms import NewCampgroundForm

class NewCampgroundFormTest(TestCase):
    def test_new_campground_form_valid(self):
        form_data = {'name': 'camp 1', 'imageUrl': 'http://www.nextcampsite.com/wp-content/uploads/2014/07/Lost-Creek-Campground-D08.jpg'}
        form = NewCampgroundForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_new_campground_form_noname_invalid(self):
        form_data_noname = {'name': '', 'imageUrl': 'http://www.nextcampsite.com/wp-content/uploads/2014/07/Lost-Creek-Campground-D08.jpg'}
        form = NewCampgroundForm(data=form_data_noname)
        self.assertFalse(form.is_valid())

    def test_new_campground_form_noimage_invalid(self):
        form_data_noimage = {'name': 'camp 1', 'imageUrl': ''}
        form = NewCampgroundForm(data=form_data_noimage)
        self.assertFalse(form.is_valid())

    def test_new_campground_form_wrongUrl_invalid(self):
        form_data_wrongUrl = {'name': 'camp 1', 'imageUrl': 'fasdfasdfasdfafds'}
        form = NewCampgroundForm(data=form_data_wrongUrl)
        self.assertFalse(form.is_valid())

