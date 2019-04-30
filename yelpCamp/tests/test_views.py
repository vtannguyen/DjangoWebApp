from django.test import TestCase
from django.contrib.auth import authenticate, login
from ..models import Campground, Comment
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from ..forms import NewCampgroundForm

# Create your tests here.
CORRECT_IMAGE_URL = 'http://www.nextcampsite.com/wp-content/uploads/2014/07/Lost-Creek-Campground-D08.jpg'
def createComment(text, campground):
    return Comment.objects.create(text=text, timestamp=timezone.now(), campground=campground)

def createUser(username='username'):
    user = User.objects.create_user(username, password='123456789')
    user.save()
    return user

def createCampground(
        user=None,
        name='camp 1',
        imageUrl=CORRECT_IMAGE_URL,
        description='this place is so nice'):
    return Campground.objects.create(name=name, imageUrl=imageUrl, description=description, user=user)

def createUserAndLogin(self, username='username'):
    user = User.objects.create_user(username)
    user.set_password('123456789')
    user.save()
    self.client.login(username=username, password='123456789')

    return user

class CampgroundViewTest(TestCase):
    def test_no_Campground(self):
        response = self.client.get(reverse('yelpCamp:campgrounds'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['campgroundList'], [])

    def test_two_Campground(self):
        createCampground(name='camp 1')
        createCampground(name='camp 2')
        response = self.client.get(reverse('yelpCamp:campgrounds'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['campgroundList'], ['<Campground: camp 2>', '<Campground: camp 1>'])


class AddNewCampgroundTest(TestCase):
    def test_open_campground_create_form_by_not_authenticated_user(self):
        response = self.client.get(reverse('yelpCamp:campgroundsNew'))
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('yelpCamp:campgroundsNew'))

    def test_open_campground_create_form_by_authenticated_user(self):
        createUserAndLogin(self)
        response = self.client.get(reverse('yelpCamp:campgroundsNew'))
        self.assertEqual(response.status_code, 200)

    def test_create_new_campground_by_authenticated_user(self):
        user = createUserAndLogin(self)
        response = self.client.post(reverse(
            'yelpCamp:campgrounds'),
            {'name': 'test Camp', 'imageUrl': CORRECT_IMAGE_URL, 'description': 'this is awesome'})

        camp_test = Campground.objects.get(name='test Camp')
        self.assertRedirects(response, reverse('yelpCamp:campgrounds'))
        self.assertEqual(camp_test.imageUrl, CORRECT_IMAGE_URL)
        self.assertEqual(camp_test.description, 'this is awesome')
        self.assertEqual(camp_test.user, user)

    def test_create_new_campground_by_not_authenticated_user(self):
        response = self.client.post(reverse(
            'yelpCamp:campgrounds'),
            {'name': 'test Camp', 'imageUrl': CORRECT_IMAGE_URL, 'description': 'this is awesome'})

        self.assertQuerysetEqual(response.context['campgroundList'], [])

    def test_create_campground_with_empty_name(self):
        createUserAndLogin(self)
        response = self.client.post(reverse(
            'yelpCamp:campgrounds'),
            {'name': '', 'imageUrl': CORRECT_IMAGE_URL, 'description': 'this is awesome'})

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Campground.objects.filter(imageUrl=CORRECT_IMAGE_URL).exists())

    def test_create_campground_with_empty_imageUrl(self):
        createUserAndLogin(self)
        response = self.client.post(reverse(
            'yelpCamp:campgrounds'),
            {'name': 'test Camp', 'imageUrl': '', 'description': 'this is awesome'})

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Campground.objects.filter(name='test Camp').exists())

    def test_create_campground_with_empty_discription(self):
        createUserAndLogin(self)
        response = self.client.post(reverse(
            'yelpCamp:campgrounds'),
            {'name': 'test Camp', 'imageUrl': CORRECT_IMAGE_URL, 'description': ''})

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Campground.objects.filter(name='test Camp').exists())


class CampgroundEditTest(TestCase):
    def test_open_campground_edit_by_unauthenticated_user(self):
        campground = createCampground()
        url = reverse('yelpCamp:campgroundEdit', args=(campground.id,))
        response = self.client.get(url)

        self.assertRedirects(response, reverse('login') + '?next=' + url)

    def test_open_campground_edit_not_by_campground_owner(self):
        campgroundOwner = User.objects.create_user(username='user1', password='123456789')
        campgroundOwner.save()
        campground = createCampground(user=campgroundOwner)
        createUserAndLogin(self, username='anotherUser')
        url = reverse('yelpCamp:campgroundEdit', args=(campground.id,))
        response = self.client.get(url)

        redirectUrl = reverse('yelpCamp:campgroundDetails', args=(campground.id,))
        self.assertRedirects(response, redirectUrl)

    def test_open_campground_edit_by_campground_owner(self):
        campgroundOwner = createUserAndLogin(self)
        campground = createCampground(user=campgroundOwner)
        url = reverse('yelpCamp:campgroundEdit', args=(campground.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, campground.imageUrl)
        self.assertContains(response, campground.name)
        self.assertContains(response, campground.description)

    def test_open_invalid_campground_to_edit(self):
        createUserAndLogin(self)
        url = reverse('yelpCamp:campgroundEdit', args=(5,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_update_campground_by_owner(self):
        campgroundOwner = createUserAndLogin(self)
        campground = createCampground(
            name='camp 1',
            imageUrl='http://www.testImage.com/testImage.jpg',
            description='this place is no nice',
            user=campgroundOwner)
        url = reverse('yelpCamp:campgroundDetails', args=(campground.id,))
        newName = 'newName'
        newImageUrl = CORRECT_IMAGE_URL
        newDescription = 'new description'

        self.client.post(url, data={
            'name': newName,
            'imageUrl': newImageUrl,
            'description': newDescription
        })

        campgroundNew = Campground.objects.get(pk=campground.id)

        self.assertEqual(campgroundNew.name, newName)
        self.assertEqual(campgroundNew.imageUrl, newImageUrl)
        self.assertEqual(campgroundNew.description, newDescription)

    def test_update_ground_not_by_owner(self):
        anotherUser = createUser(username='anotherUser')
        createUserAndLogin(self)
        campground = createCampground(
            name='camp 1',
            imageUrl='http://www.testImage.com/testImage.jpg',
            description='this place is no nice',
            user=anotherUser)
        url = reverse('yelpCamp:campgroundDetails', args=(campground.id,))
        newName = 'newName'
        newImageUrl = CORRECT_IMAGE_URL
        newDescription = 'new description'

        response = self.client.post(url, {
            'name': newName,
            'imageUrl': newImageUrl,
            'description': newDescription
        })
        campgroundNew = Campground.objects.get(pk=campground.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(campgroundNew.name, campground.name)
        self.assertEqual(campgroundNew.imageUrl, campground.imageUrl)
        self.assertEqual(campgroundNew.description, campground.description)

    def test_delete_campground_by_owner(self):
        campgroundOwner = createUserAndLogin(self)
        campground = createCampground(user=campgroundOwner)
        url = reverse('yelpCamp:campgroundDetails', args=(campground.id,))

        response = self.client.delete(url)

        self.assertFalse(Campground.objects.filter(pk=campground.id).exists())
        self.assertRedirects(response, reverse('yelpCamp:campgrounds'))

    def test_delete_campground_not_by_owner(self):
        anotherUser = createUser(username='anotherUser')
        createUserAndLogin(self)
        campground = createCampground(user=anotherUser)
        url = reverse('yelpCamp:campgroundDetails', args=(campground.id,))

        response = self.client.delete(url)

        self.assertTrue(Campground.objects.filter(pk=campground.id).exists())
        self.assertRedirects(response, reverse('yelpCamp:campgrounds'))


class CampgroundDetailsViewTest(TestCase):
    def test_campground_with_comment(self):
        campground = createCampground(name='camp 1', imageUrl=CORRECT_IMAGE_URL)
        createComment(text='this is comment', campground=campground)

        response = self.client.get(reverse('yelpCamp:campgroundDetails', args=(campground.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['campground'], campground)
        self.assertQuerysetEqual(response.context['comments'], ['<Comment: this is comment>'])

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


class CommentNewViewTest(TestCase):
    def test_open_add_comment_page_by_not_authenticated_user(self):
        camp_test = createCampground(name='camp 1', imageUrl=CORRECT_IMAGE_URL)
        url = reverse('yelpCamp:commentsNew', args=(camp_test.id,))
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    def test_open_add_comment_page_by_authenticated_user(self):
        createUserAndLogin(self)
        camp_test = createCampground(name='camp 1', imageUrl=CORRECT_IMAGE_URL)
        url = reverse('yelpCamp:commentsNew', args=(camp_test.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, camp_test.id)

    def test_add_comment_to_database_by_authenticated_user(self):
        user = createUserAndLogin(self)
        camp_test = createCampground(name='camp 1', imageUrl=CORRECT_IMAGE_URL)
        COMMENT = 'this is test comment'
        url = reverse('yelpCamp:comments', args=(camp_test.id,))
        response = self.client.post(url, {'text': COMMENT})
        comment = Comment.objects.get(text__exact=COMMENT)

        redirectUrl = reverse('yelpCamp:campgroundDetails', args=(camp_test.id,))
        self.assertRedirects(response, redirectUrl)
        self.assertEqual(comment.campground.id, camp_test.id)
        self.assertEqual(comment.user, user)

    def test_add_comment_to_database_by_not_authenticated_user(self):
        camp_test = createCampground(name='camp 1', imageUrl=CORRECT_IMAGE_URL)
        COMMENT = 'this is test comment'
        url = reverse('yelpCamp:comments', args=(camp_test.id,))
        response = self.client.post(url, {'text': COMMENT})

        redirectUrl = reverse('yelpCamp:campgroundDetails', args=(camp_test.id,))
        self.assertRedirects(response, redirectUrl)

    def test_send_get_request_to_add_comment_route(self):
        camp_test = createCampground(name='camp 1', imageUrl=CORRECT_IMAGE_URL)
        url = reverse('yelpCamp:comments', args=(camp_test.id,))
        response = self.client.get(url)
        redirectUrl = reverse('yelpCamp:campgroundDetails', args=(camp_test.id,))
        self.assertRedirects(response, redirectUrl)

    def test_add_empty_comment(self):
        createUserAndLogin(self)
        camp_test = createCampground(name='camp 1', imageUrl=CORRECT_IMAGE_URL)
        COMMENT = ''
        url = reverse('yelpCamp:comments', args=(camp_test.id,))
        self.client.post(url, {'text': COMMENT})

        self.assertFalse(Comment.objects.filter(text__exact=COMMENT).exists())


class AuthenticationTest(TestCase):
    def test_sign_up_valid(self):
        url = reverse('yelpCamp:userSignup')
        response = self.client.post(url, {
            'username': 'test1',
            'password1': 'test123456',
            'password2': 'test123456',
        })

        self.assertRedirects(response, reverse('yelpCamp:campgrounds'))
        self.assertTrue(User.objects.filter(username__exact='test1').exists())

    def test_sign_up_mismatch_password(self):
        url = reverse('yelpCamp:userSignup')
        form_data = {
            'username': 'test1',
            'password1': 'test12345',
            'password2': 'test123456',
        }
        self.client.post(url, form_data)

        self.assertFalse(User.objects.filter(username__exact='test1'))

    def test_sign_up_same_username_twice(self):
        url = reverse('yelpCamp:userSignup')
        self.client.post(url, {
            'username': 'test1',
            'password1': 'test123456',
            'password2': 'test123456',
        })
        user1st = User.objects.get(username__exact='test1')
        self.client.post(url, {
            'username': 'test1',
            'password1': 'test12345',
            'password2': 'test12345',
        })
        user2nd = User.objects.get(username__exact='test1')
        self.assertEqual(user1st.password, user2nd.password)

    def test_open_sign_up_form(self):
        response = self.client.get(reverse('yelpCamp:userSignup'))
        self.assertEqual(response.status_code, 200)


class IndexViewTest(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('yelpCamp:landing'))
        self.assertEqual(response.status_code, 200)

