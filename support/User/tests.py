from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, APITestCase, APIClient
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from User import views
from User.models import User


class AccountTest(APITestCase):
    """Testing the API for the user"""
    def setUp(self):

        self.factory = APIRequestFactory()
        # User data for registration
        self.user_data = {
            "login": "test_user",
            "password" : "12345",
            "email": "testmail@mail.ru",

            "_comment": "This key and the lower keys are optional !",
            "first_name": "test_user_first",
            "last_name": "test_user_last"
        }
        # User registration
        self.response = self.client.post(reverse('create_user'), self.user_data, format='json')

    def test_create_account(self):
        """Checks the data in the returned response and the data recorded in the database."""

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(self.response.content, bytes)

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().login, self.user_data['login'])
        self.assertEqual(User.objects.get().email, self.user_data['email'])
        self.assertEqual(User.objects.get().first_name, self.user_data['first_name'])
        self.assertEqual(User.objects.get().last_name, self.user_data['last_name'])
        self.assertTrue(User.objects.get().check_password(self.user_data['password']))

        self.assertEqual(self.response.data['login'], self.user_data['login'])
        self.assertEqual(self.response.data['email'], self.user_data['email'])
        self.assertEqual(self.response.data['first_name'], self.user_data['first_name'])
        self.assertEqual(self.response.data['last_name'], self.user_data['last_name'])
        self.assertNotIn("_comment", self.response.data)

    def test_obtain_token(self):
        url = reverse('obtain_token')

        response = self.client.post(url,
                                    {'login': self.user_data['login'], 'password': self.user_data['password']},
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.content, bytes)

        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)


    def _get_tokens(self):

        response = self.client.post(reverse('obtain_token'),
                                                 {'login': self.user_data['login'],
                                                  'password': self.user_data['password']},
                                                 format='json')

        return {"refresh_token": response.data['refresh'], "access_token": response.data['access'] }

    def test_refresh_token(self):
        """Checks token access update."""

        tokens = self._get_tokens()

        url = reverse('refresh_token')
        response = self.client.post(url,
                                    {'refresh': tokens['refresh_token']},
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.content, bytes)

        self.assertIn('access', response.data)
        self.assertNotEqual(tokens['access_token'], response.data['access'])


    def test_verify_token(self):
        """Token access verification."""
        tokens = self._get_tokens()

        url = reverse('verify_token')
        response = self.client.post(url,
                                    {'token': tokens['access_token']},
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_data(self):
        """Checking for user data retrieval."""

        tokens = self._get_tokens()
        url = reverse(f"update-data",args=[self.response.data['id']])

        # self.client.login(login=self.user_data['login'], password=self.user_data['password'])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + tokens['access_token'])

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.content, bytes)

        self.assertEqual(response.data['login'], self.user_data['login'])
        self.assertEqual(response.data['first_name'], self.user_data['first_name'])
        self.assertEqual(response.data['last_name'], self.user_data['last_name'])
        self.assertEqual(response.data['email'], self.user_data['email'])
        self.assertEqual(len(response.data), 4)

    def test_put_user_data(self):
        """Checks for changes in user data."""
        new_data = {
            "_coment": "This key and the lower keys are optional !",

            "login": "user1",
            "first_name": "user1_frist",
            "last_name": "user1_lust",
            "email": "zarjrw1994@gmail.com"

        }

        tokens = self._get_tokens()
        url = reverse(f"update-data", args=[self.response.data['id']])

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + tokens['access_token'])

        response = self.client.get(url, new_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.content, bytes)

        self.assertNotEqual(response.data['first_name'], new_data['first_name'])
        self.assertNotEqual(response.data['last_name'], new_data['last_name'])
        self.assertNotEqual(response.data['email'], new_data['email'])
        self.assertNotIn("_comment", self.response.data)

    def test_change_password(self):
        """Tests if the user changes the password."""

        tokens = self._get_tokens()
        url = reverse('change_password', args=[self.response.data['id']])
        change_password_data = {
                                "old_password": self.user_data['password'],
                                "password": "a12345"
                                }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + tokens['access_token'])

        response = self.client.put(url, change_password_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.content, bytes)

        self.assertEqual(response.data['id'], self.response.data['id'])

    def test_get_all_users(self):
        """Returns all users ."""
        tokens = self._get_tokens()

        url = reverse('all_users')

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + tokens['access_token'])
        user = User.objects.get(pk=self.response.data['id'])
        user.is_support = True
        user.save()

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.content, bytes)


        self.assertGreaterEqual(len(response.data), 0)

    def test_get_only_support(self):
        """Enables all users with "support" status"""

        tokens = self._get_tokens()
        url = reverse('only_support')

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + tokens['access_token'])
        user = User.objects.get(pk=self.response.data['id'])
        user.is_staff = True
        user.is_support = True
        user.save()

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.content, bytes)

        self.assertTrue(len(response.data) >= 1, "Support list is empty")

    def test_support_control(self):
        """Checks if the user is a support. Available for administrators only."""

        user_tokens = self._get_tokens()
        url = reverse('support_control', args=[self.response.data['id']])

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_tokens['access_token'])
        user_response = self.client.get(url, format='json')

        self.assertEqual(user_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIsInstance(user_response.content, bytes)
        self.assertEqual(user_response.data['errors'][0]['code'], 'permission_denied')


        user = User.objects.get(pk=self.response.data['id'])
        user.is_staff = True
        user.save()

        user_response2 = self.client.get(url, format='json')
        self.assertEqual(user_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIsInstance(user_response.content, bytes)

        self.assertIn('id' ,user_response2.data)
        self.assertIn('login', user_response2.data)
        self.assertIn('is_support', user_response2.data)




