import json

from django.urls import reverse

from rest_framework.test import APITestCase

# Create your tests here.


class UserRegistrationTest(APITestCase):
    url = reverse('users:registration')

    def test_can_registration(self):
        """유저가 제대로 생성되는지 테스트"""
        user_data = {
            "username": "testuesr",
            "email": "test@testuser.com",
            "password": "test1234",
            "confirm_password": "test1234",
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue('token' in json.loads(response.content))
