from django.test import TestCase
from ..forms import NewCampgroundForm, NewCommentForm, SignUpForm

CORRECT_IMAGE_URL = 'http://www.nextcampsite.com/wp-content/uploads/2014/07/Lost-Creek-Campground-D08.jpg'


class NewCampgroundFormTest(TestCase):
    def setUp(self):
        def createCampgroundForm(
                name='camp 1',
                imageUrl=CORRECT_IMAGE_URL,
                description='This campground is beautiful',
                price=1.0
        ):
            form_data = {'name': name, 'imageUrl': imageUrl, 'description': description, 'price': price}
            return NewCampgroundForm(data=form_data)

        self.createCampgroundForm = createCampgroundForm

    def tearDown(self):
        del self.createCampgroundForm

    def test_new_campground_form_valid(self):
        form = self.createCampgroundForm()
        self.assertTrue(form.is_valid())

    def test_new_campground_form_noname(self):
        form = self.createCampgroundForm(name=None)
        self.assertFalse(form.is_valid())

    def test_new_campground_form_noimage(self):
        form = self.createCampgroundForm(imageUrl='')
        self.assertFalse(form.is_valid())

    def test_new_campground_form_wrongUrl(self):
        form = self.createCampgroundForm(imageUrl='invalidUrl')
        self.assertFalse(form.is_valid())

    def test_new_campground_from_noDescription(self):
        form = self.createCampgroundForm(description='')
        self.assertFalse(form.is_valid())


class NewCommentFormTest(TestCase):
    def setUp(self):
        def createCommentForm(text='this is a comment'):
            form_data = {'text': text}
            return NewCommentForm(data=form_data)

        self.createCommentForm = createCommentForm

    def tearDown(self):
        del self.createCommentForm

    def test_new_comment_form_valid(self):
        form = self.createCommentForm()
        self.assertTrue(form.is_valid())

    def test_new_comment_form_invalid(self):
        form = self.createCommentForm(text='')
        self.assertFalse(form.is_valid())


class UserSignupFormTest(TestCase):
    def setUp(self):
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

        self.createUserSignupForm = createUserSignupForm

    def tearDown(self):
        del self.createUserSignupForm

    def test_valid_user_signup_form(self):
        form = self.createUserSignupForm()
        self.assertTrue(form.is_valid())

    def test_invalid_email_address(self):
        form = self.createUserSignupForm(email='notanemail')
        self.assertFalse(form.is_valid())

    def test_no_first_name(self):
        form = self.createUserSignupForm(first_name='')
        self.assertTrue(form.is_valid())

    def test_no_last_name(self):
        form = self.createUserSignupForm(last_name='')
        self.assertTrue(form.is_valid())
