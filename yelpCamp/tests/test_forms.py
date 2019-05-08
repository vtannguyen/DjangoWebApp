from django.test import TestCase
from ..forms import NewCampgroundForm, NewCommentForm, SignUpForm

CORRECT_IMAGE_URL = 'http://www.nextcampsite.com/wp-content/uploads/2014/07/Lost-Creek-Campground-D08.jpg'
def createUserSignupForm(
        username='username',
        email='example@gmail.com',
        first_name='Michael',
        last_name='Lee',
        password1='random123456',
        password2='random123456',
        ):
    form_data = {
        'username': username,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'password1': password1,
        'password2': password2
    }
    return SignUpForm(data=form_data)

class NewCampgroundFormTest(TestCase):
    def test_new_campground_form_valid(self):
        form_data = {
            'name': 'camp 1',
            'imageUrl': CORRECT_IMAGE_URL,
            'description': 'This campground is beautiful',
            'price': 1.0
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

class NewCommentFormTest(TestCase):
    def test_new_comment_form_valid(self):
        form_data = {'text': 'this is a comment'}
        form = NewCommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_new_comment_form_invalid(self):
        form_data = {'text': ''}
        form = NewCommentForm(data=form_data)
        self.assertFalse(form.is_valid())

class UserSignupFormTest(TestCase):
    def test_valid_user_signup_form(self):
        form = createUserSignupForm()
        self.assertTrue(form.is_valid())

    def test_invalid_email_address(self):
        form = createUserSignupForm(email='notanemail')
        self.assertFalse(form.is_valid())

    def test_no_first_name(self):
        form = createUserSignupForm(first_name='')
        self.assertTrue(form.is_valid())

    def test_no_last_name(self):
        form = createUserSignupForm(last_name='')
        self.assertTrue(form.is_valid())
