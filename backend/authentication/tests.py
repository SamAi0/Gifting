from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'test@example.com'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.login_url = reverse('token_obtain_pair')
        self.profile_url = reverse('auth_profile')
        self.logout_url = reverse('logout')

    def test_login_sets_cookie(self):
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.cookies)
        self.assertIn('refresh_token', response.cookies)

    def test_profile_access_with_cookie(self):
        # Login first to get cookies
        login_response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        
        # Access profile
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user_data['username'])

    def test_logout_clears_cookie(self):
        # Login first
        self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        
        # Logout
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if cookies are deleted (max-age=0 or empty)
        self.assertEqual(response.cookies['access_token'].value, '')
