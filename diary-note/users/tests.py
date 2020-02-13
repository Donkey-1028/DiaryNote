from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

# Create your tests here.


class UserRegistrationTest(APITestCase):
    url = reverse('users:registration')

    def setUp(self):
        self.user_data = {
            "username": "testuesr",
            "email": "test@testuser.com",
            "password": "test1234",
            "confirm_password": "test1234",
        }

    def test_can_registration(self):
        """유저가 제대로 생성되는지 테스트"""
        response = self.client.post(self.url, self.user_data)
        print(response.data.get('id'))
        self.assertEqual(response.status_code, 201)

    def test_make_token_automatically(self):
        """유저가 생성되었을 때 토큰이 자동으로 생성되는지"""
        response = self.client.post(self.url, self.user_data)
        user_id = response.data.get('id')
        token = Token.objects.get(user_id=user_id)
        self.assertEqual(token.user.id, user_id)


