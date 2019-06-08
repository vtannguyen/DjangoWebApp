from django.test import TestCase
from django.contrib.auth import authenticate, login
from ..models import Campground, Comment
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

# Create your tests here.
CORRECT_IMAGE_URL = 'http://www.nextcampsite.com/wp-content/uploads/2014/07/Lost-Creek-Campground-D08.jpg'
def createComment(text, campground):
    return Comment.objects.create(text=text, timestamp=timezone.now(), campground=campground)

def createUser(username='username', password='123456789', email='example@gmail.com', first_name='Michael', last_name='Lee'):
    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
    user.save()
    return user

def createCampground(
        user=None,
        name='camp 1',
        imageUrl=CORRECT_IMAGE_URL,
        description='this place is so nice',
        price=10.01):
    return Campground.objects.create(name=name, imageUrl=imageUrl, description=description, user=user, price=price)

def createUserAndLogin(self, username='username', password='123456789', email='example@gmail.com', first_name='Michael', last_name='Lee'):
    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
    user.save()
    self.client.login(username=username, password=password)

    return user


class CampgroundViewTest(TestCase):
    def test_no_Campground(self):
        response = self.client.get(reverse('yelpCamp:campgrounds'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['campgrounds'], [])

    def test_two_Campground(self):
        createCampground(name='camp 1')
        createCampground(name='camp 2')
        response = self.client.get(reverse('yelpCamp:campgrounds'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['campgrounds'], ['<Campground: camp 2>', '<Campground: camp 1>'])
        self.assertEqual(response.context['campgrounds'].paginator.per_page, 8)


class AddNewCampgroundByAuthenticatedUserTest(TestCase):
    def setUp(self):
        self.user = createUserAndLogin(self)
        self.campgroundListUrl = reverse('yelpCamp:campgrounds')
        self.campground = {'name': 'test Camp', 'imageUrl': CORRECT_IMAGE_URL, 'description': 'this is awesome', 'price': 10.20}
        def sendCreationRequest(
                name=self.campground['name'],
                imageUrl=self.campground['imageUrl'],
                description=self.campground['description'],
                price=self.campground['price']
            ):
            return self.client.post(self.campgroundListUrl, {'name': name, 'imageUrl': imageUrl, 'description': description, 'price': price})
        self.sendCreationRequest = sendCreationRequest

    def tearDown(self):
        del self.user
        del self.campground
        del self.campgroundListUrl
        del self.sendCreationRequest

    def test_open_campground_create_form_by_authenticated_user(self):
        response = self.client.get(reverse('yelpCamp:campgroundsNew'))
        self.assertEqual(response.status_code, 200)

    def test_create_new_campground_by_authenticated_user(self):
        response = self.sendCreationRequest()

        camp_test = Campground.objects.get(name=self.campground['name'])
        self.assertRedirects(response, self.campgroundListUrl)
        self.assertEqual(camp_test.imageUrl, self.campground['imageUrl'])
        self.assertEqual(camp_test.description, self.campground['description'])
        self.assertEqual(camp_test.user, self.user)
        self.assertEqual(float(camp_test.price), self.campground['price'])

    def test_create_campground_with_empty_name(self):
        response = self.sendCreationRequest(name='')

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Campground.objects.filter(imageUrl=self.campground['imageUrl']).exists())

    def test_create_campground_with_empty_imageUrl(self):
        response = self.sendCreationRequest(imageUrl='')

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Campground.objects.filter(name=self.campground['name']).exists())

    def test_create_campground_with_empty_description(self):
        response = self.sendCreationRequest(description='')

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Campground.objects.filter(name=self.campground['name']).exists())

    def test_create_campground_with_empty_price(self):
        response = self.client.post(
            self.campgroundListUrl,
            {'name': self.campground['name'], 'imageUrl': self.campground['imageUrl'], 'description': self.campground['description']})

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Campground.objects.filter(name=self.campground['name']).exists())


class AddNewCampgroundByUnauthenticatedUserTest(TestCase):
    def test_open_campground_create_form_by_not_authenticated_user(self):
        response = self.client.get(reverse('yelpCamp:campgroundsNew'))
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('yelpCamp:campgroundsNew'))

    def test_create_new_campground_by_not_authenticated_user(self):
        response = self.client.post(reverse(
            'yelpCamp:campgrounds'),
            {'name': 'test Camp', 'imageUrl': CORRECT_IMAGE_URL, 'description': 'this is awesome'})

        self.assertQuerysetEqual(response.context['campgrounds'], [])


class CampgroundEditByOwnerTest(TestCase):
    def setUp(self):
        self.campgroundOwner = createUserAndLogin(self)
        self.campground = createCampground(user=self.campgroundOwner)
        self.campgroundDetailsUrl = reverse('yelpCamp:campgroundDetails', args=(self.campground.id,))
        self.campgroundEditUrl = reverse('yelpCamp:campgroundEdit', args=(self.campground.id,))

    def tearDown(self):
        del self.campgroundOwner
        del self.campground
        del self.campgroundDetailsUrl
        del self.campgroundEditUrl

    def test_open_campground_edit_by_campground_owner(self):
        response = self.client.get(self.campgroundEditUrl)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campground.imageUrl)
        self.assertContains(response, self.campground.name)
        self.assertContains(response, self.campground.description)
        self.assertContains(response, self.campground.price)


    def test_update_campground_by_owner(self):
        newCampgroundData = {
            'name': 'newName',
            'imageUrl': CORRECT_IMAGE_URL,
            'description': 'new description',
            'price': 5.0
        }

        self.client.post(self.campgroundDetailsUrl, data=newCampgroundData)
        campgroundNew = Campground.objects.get(pk=self.campground.id)

        self.assertEqual(campgroundNew.name, newCampgroundData['name'])
        self.assertEqual(campgroundNew.imageUrl, newCampgroundData['imageUrl'])
        self.assertEqual(campgroundNew.description, newCampgroundData['description'])
        self.assertEqual(campgroundNew.price, newCampgroundData['price'])

    def test_delete_campground_by_owner(self):
        response = self.client.delete(self.campgroundDetailsUrl)

        self.assertFalse(Campground.objects.filter(pk=self.campground.id).exists())
        self.assertRedirects(response, reverse('yelpCamp:campgrounds'))


class CampgroundEditMiscellaneousTest(TestCase):
    def test_open_campground_edit_by_unauthenticated_user(self):
        campground = createCampground()
        url = reverse('yelpCamp:campgroundEdit', args=(campground.id,))
        response = self.client.get(url)

        self.assertRedirects(response, reverse('login') + '?next=' + url)


class CampgroundEditNotByOwnerTest(TestCase):
    def setUp(self):
        self.campgroundOwner = User.objects.create_user(username='user1', password='123456789')
        self.campground = createCampground(user=self.campgroundOwner)
        self.camgroundDetailsRoute = reverse('yelpCamp:campgroundDetails', args=(self.campground.id,))
        self.anotherUser = createUserAndLogin(self, username='anotherUser')

    def tearDown(self):
        del self.campground
        del self.campgroundOwner
        del self.camgroundDetailsRoute
        del self.anotherUser

    def test_open_campground_edit_not_by_campground_owner(self):
        url = reverse('yelpCamp:campgroundEdit', args=(self.campground.id,))
        response = self.client.get(url)

        self.assertRedirects(response, self.camgroundDetailsRoute)

    def test_open_invalid_campground_to_edit(self):
        url = reverse('yelpCamp:campgroundEdit', args=(5,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_update_ground_not_by_owner(self):
        newCampgroundData = {
            'name': 'newName',
            'imageUrl': CORRECT_IMAGE_URL,
            'description': 'new description',
        }

        response = self.client.post(self.camgroundDetailsRoute, newCampgroundData)
        campgroundNew = Campground.objects.get(pk=self.campground.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(campgroundNew.name, self.campground.name)
        self.assertEqual(campgroundNew.imageUrl, self.campground.imageUrl)
        self.assertEqual(campgroundNew.description, self.campground.description)

    def test_delete_campground_not_by_owner(self):
        response = self.client.delete(self.camgroundDetailsRoute)

        self.assertTrue(Campground.objects.filter(pk=self.campground.id).exists())
        self.assertRedirects(response, reverse('yelpCamp:campgrounds'))


class CampgroundDetailsViewTest(TestCase):
    def setUp(self):
        self.campground = createCampground(name='camp 1', imageUrl=CORRECT_IMAGE_URL)
        self.campgroundUrl = reverse('yelpCamp:campgroundDetails', args=(self.campground.id,))

    def tearDown(self):
        del self.campground
        del self.campgroundUrl

    def test_campground_with_comment(self):
        createComment(text='this is comment', campground=self.campground)

        response = self.client.get(self.campgroundUrl)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['campground'], self.campground)
        self.assertQuerysetEqual(response.context['comments'], ['<Comment: this is comment>'])
        self.assertEqual(response.context['comments'].paginator.per_page, 4)

    def test_incorrect_campground_id(self):
        url = reverse('yelpCamp:campgroundDetails', args=(5,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_correct_campground_id(self):
        response = self.client.get(self.campgroundUrl)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campground.name)
        self.assertContains(response, self.campground.imageUrl)
        self.assertContains(response, self.campground.description)


class AddCommentByAuthenticatedUserTest(TestCase):
    def setUp(self):
        self.user = createUserAndLogin(self)
        self.camp_test = createCampground(name='camp 1', imageUrl=CORRECT_IMAGE_URL)
        def sendAddCommentRequest(comment):
            url = reverse('yelpCamp:comments', args=(self.camp_test.id,))
            return self.client.post(url, {'text': comment})
        self.sendAddCommentRequest = sendAddCommentRequest

    def tearDown(self):
        del self.user
        del self.sendAddCommentRequest

    def test_add_comment_to_database_by_authenticated_user(self):
        COMMENT = 'this is test comment'
        response = self.sendAddCommentRequest(comment=COMMENT)
        comment = Comment.objects.get(text__exact=COMMENT)

        redirectUrl = reverse('yelpCamp:campgroundDetails', args=(self.camp_test.id,))
        self.assertRedirects(response, redirectUrl)
        self.assertEqual(comment.campground.id, self.camp_test.id)
        self.assertEqual(comment.user, self.user)

    def test_add_empty_comment(self):
        COMMENT = ''
        self.sendAddCommentRequest(comment=COMMENT)

        self.assertFalse(Comment.objects.filter(text__exact=COMMENT).exists())

    def test_open_add_comment_page_by_authenticated_user(self):
        url = reverse('yelpCamp:commentsNew', args=(self.camp_test.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.camp_test.id)



class CommentNewViewTest(TestCase):
    def setUp(self):
        self.camp_test = createCampground(name='camp 1', imageUrl=CORRECT_IMAGE_URL)
        self.addCommentUrl = reverse('yelpCamp:comments', args=(self.camp_test.id,))
        self.redirectUrl = reverse('yelpCamp:campgroundDetails', args=(self.camp_test.id,))

    def tearDown(self):
        del self.camp_test
        del self.addCommentUrl
        del self.redirectUrl

    def test_open_add_comment_page_by_not_authenticated_user(self):
        url = reverse('yelpCamp:commentsNew', args=(self.camp_test.id,))
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    def test_add_comment_to_database_by_not_authenticated_user(self):
        COMMENT = 'this is test comment'
        response = self.client.post(self.addCommentUrl, {'text': COMMENT})

        self.assertRedirects(response, self.redirectUrl)

    def test_send_get_request_to_add_comment_route(self):
        response = self.client.get(self.addCommentUrl)
        self.assertRedirects(response, self.redirectUrl)



class AuthenticationTest(TestCase):
    def setUp(self):
        self.user = {
            'username': 'test1',
            'email': 'example@gmail.com',
            'first_name': 'Michael',
            'last_name': 'Lee',
            'password1': 'test123456',
            'password2': 'test123456',
        }
        def sendUserCreationRequest(
                name=self.user['username'],
                email=self.user['email'],
                first_name=self.user['first_name'],
                last_name=self.user['last_name'],
                password1=self.user['password1'],
                password2=self.user['password2']):
            signupUrl = reverse('yelpCamp:userSignup')
            return self.client.post(signupUrl, {
                'username': name,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'password1': password1,
                'password2': password2})
        self.sendUserCreationRequest = sendUserCreationRequest

    def tearDown(self):
        del self.user
        del self.sendUserCreationRequest

    def test_sign_up_valid(self):
        response = self.sendUserCreationRequest()
        self.assertRedirects(response, reverse('yelpCamp:campgrounds'))
        self.assertTrue(User.objects.filter(username__exact=self.user['username']).exists())
        user = User.objects.get(username__exact=self.user['username'])
        self.assertEqual(user.email, self.user['email'])
        self.assertEqual(user.first_name, self.user['first_name'])
        self.assertEqual(user.last_name, self.user['last_name'])

    def test_sign_up_mismatch_password(self):
        self.sendUserCreationRequest(password1='test12345')

        self.assertFalse(User.objects.filter(username__exact=self.user['username']))

    def test_sign_up_same_username_twice(self):
        self.sendUserCreationRequest()
        user1st = User.objects.get(username__exact=self.user['username'])
        self.sendUserCreationRequest(password1='helo12345', password2='hello12345')
        user2nd = User.objects.get(username__exact=self.user['username'])
        self.assertEqual(user1st.password, user2nd.password)

    def test_open_sign_up_form(self):
        response = self.client.get(reverse('yelpCamp:userSignup'))
        self.assertEqual(response.status_code, 200)


class IndexViewTest(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('yelpCamp:landing'))
        self.assertEqual(response.status_code, 200)


class UserAuthenticationTest(TestCase):
    def setUp(self):
        self.password = 'password123456'
        self.user = createUser(password=self.password)

    def tearDown(self):
        del self.password
        del self.user

    def test_log_in_with_valid_username_and_password(self):
        self.client.login(username=self.user.username, password=self.password)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)

    def test_log_in_with_valid_email_and_password(self):
        self.client.login(username=self.user.email, password=self.password)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)

    def test_log_in_with_valid_username_and_invalid_password(self):
        self.client.login(username=self.user.username, password=self.password+'lorem')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_log_in_with_valid_email_and_invalid_password(self):
        self.client.login(username=self.user.email, password=self.password+'lorem')
        self.assertNotIn('_auth_user_id', self.client.session)

