from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

# Create your tests here.


class UserRegistrationAPIViewTest(APITestCase):
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
        self.assertEqual(response.status_code, 201)

    def test_make_token_automatically(self):
        """유저가 생성되었을 때 토큰이 자동으로 생성되는지 테스트"""
        response = self.client.post(self.url, self.user_data)
        user_id = response.data.get('id')
        token = Token.objects.get(user_id=user_id)
        self.assertEqual(token.user.id, user_id)

    def test_invalid_password(self):
        """유저 생성시 비밀번호와 비밀번호 확인을 다르게 하였을때 valid 에러가 발생하는지 테스트"""
        user_data = {
            "username": "testuesr",
            "email": "test@testuser.com",
            "password": "test1234",
            "confirm_password": "invalid_password",
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(response.status_code, 400)


class UserLoginAPIViewTest(APITestCase):
    url = reverse('users:login')

    def setUp(self):
        self.username = "testuser"
        self.password = "test1234"
        self.email = "test1234@test.com"
        self.user = User.objects.create_user(username=self.username, password=self.password,
                                             email=self.email)

    def test_user_try_login_with_wrong_password(self):
        """비밀번호가 잘못 되었을 때 테스트"""
        response = self.client.post(self.url, {"username": "testuser", "password": "1234test"})
        self.assertEqual(response.status_code, 400)

    def test_user_try_login_with_wrong_username(self):
        """username이 잘못 되었을 때 테스트"""
        response = self.client.post(self.url, {"username": "usertest", "password": "test1234"})
        self.assertEqual(response.status_code, 400)

    def test_user_successfully_login(self):
        """정상적으로 login 했을 때 테스트"""
        response = self.client.post(self.url, {"username": "testuser", "password": "test1234"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('key' in response.data)





