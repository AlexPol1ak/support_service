from django.test import TestCase
from django.urls import reverse
from rest_framework import status
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

    def test_get_data(self):
        """Checking for user data retrieval."""

        tokens = self._get_tokens()
        url = reverse(f"update-data",args=[self.response.data['id']])

        self.client.login(login=self.user_data['login'], password=self.user_data['password'])
        # self.client.credentials(Authorization='Bearer ' + tokens['access_token'])!!!

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.content, bytes)

        self.assertEqual(response.data['login'], self.user_data['login'])
        self.assertEqual(response.data['first_name'], self.user_data['first_name'])
        self.assertEqual(response.data['last_name'], self.user_data['last_name'])
        self.assertEqual(response.data['email'], self.user_data['email'])
        self.assertEqual(len(response.data), 4)

    def p_test_put_data(self):
        new_data = {
            "_coment": "This key and the lower keys are optional !",

            "login": "user1",
            "first_name": "first_user1",
            "last_name": "last_user1",
            "email": "zarjrw1994@gmail.com"

        }