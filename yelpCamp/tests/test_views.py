from django.test import TestCase
from ..models import Campground, Comment
from django.urls import reverse
from django.utils import timezone
from ..forms import NewCampgroundForm

# Create your tests here.
CORRECT_IMAGE_URL = 'http://www.nextcampsite.com/wp-content/uploads/2014/07/Lost-Creek-Campground-D08.jpg'
def createCampground(name, imageUrl):
    return Campground.objects.create(name=name, imageUrl=imageUrl)
def createComment(text, campground):
    return Comment.objects.create(text=text, timestamp=timezone.now(), campground=campground)


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


class CampgroundDetailsTest(TestCase):
    def test_campground_with_command(self):
        campground = createCampground(name='camp 1', imageUrl=CORRECT_IMAGE_URL)
        createComment(text='this is comment', campground=campground)

        response = self.client.get(reverse('yelpCamp:campgroundDetails', args=(campground.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['campground'], campground)
        self.assertQuerysetEqual(response.context['comments'], ['<Comment: this is comment>'])


class AddNewCampgroundTest(TestCase):
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

    def test_create_campground_with_empty_name(self):
        response = self.client.post(reverse(
            'yelpCamp:campgrounds'),
            {'name': '', 'imageUrl': CORRECT_IMAGE_URL, 'description': 'this is awesome'})

        self.assertRedirects(response, reverse('yelpCamp:campgroundsNew'), status_code=302, target_status_code=200)
        self.assertFalse(Campground.objects.filter(imageUrl=CORRECT_IMAGE_URL).exists())

    def test_create_campground_with_empty_imageUrl(self):
        response = self.client.post(reverse(
            'yelpCamp:campgrounds'),
            {'name': 'test Camp', 'imageUrl': '', 'description': 'this is awesome'})

        self.assertRedirects(response, reverse('yelpCamp:campgroundsNew'), status_code=302, target_status_code=200)
        self.assertFalse(Campground.objects.filter(name='test Camp').exists())

    def test_create_campground_with_empty_discription(self):
        response = self.client.post(reverse(
            'yelpCamp:campgrounds'),
            {'name': 'test Camp', 'imageUrl': CORRECT_IMAGE_URL, 'description': ''})

        self.assertRedirects(response, reverse('yelpCamp:campgroundsNew'), status_code=302, target_status_code=200)
        self.assertFalse(Campground.objects.filter(name='test Camp').exists())


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

class CommentNewViewTest(TestCase):
    def test_open_add_comment_page(self, ):
        camp_test = createCampground(name='camp 1', imageUrl=CORRECT_IMAGE_URL)
        url = reverse('yelpCamp:commentsNew', args=(camp_test.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_comment_to_database(self):
        camp_test = createCampground(name='camp 1', imageUrl=CORRECT_IMAGE_URL)
        COMMENT = 'this is test comment'
        url = reverse('yelpCamp:comments', args=(camp_test.id,))
        response = self.client.post(url, {'text': COMMENT})
        comment = Comment.objects.get(text__exact=COMMENT)

        redirectUrl = reverse('yelpCamp:campgroundDetails', args=(camp_test.id,))
        self.assertRedirects(response, redirectUrl, status_code=302, target_status_code=200)
        self.assertEqual(comment.campground.id, camp_test.id)

    def test_send_get_request_to_add_comment_route(self):
        camp_test = createCampground(name='camp 1', imageUrl=CORRECT_IMAGE_URL)
        url = reverse('yelpCamp:comments', args=(camp_test.id,))
        response = self.client.get(url)
        redirectUrl = reverse('yelpCamp:campgroundDetails', args=(camp_test.id,))
        self.assertRedirects(response, redirectUrl, status_code=302, target_status_code=200)

    def test_create_empty_comment(self):
        camp_test = createCampground(name='camp 1', imageUrl=CORRECT_IMAGE_URL)
        COMMENT = ''
        url = reverse('yelpCamp:comments', args=(camp_test.id,))
        response = self.client.post(url, {'text': COMMENT})

        redirectUrl = reverse('yelpCamp:campgroundsNew')
        self.assertRedirects(response, redirectUrl, status_code=302, target_status_code=200)
        self.assertFalse(Comment.objects.filter(text__exact=COMMENT).exists())

