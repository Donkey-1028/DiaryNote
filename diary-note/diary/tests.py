import datetime

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from .models import Diary


class DiaryListTest(APITestCase):
    url = reverse('diary:diary_list')

    def setUp(self):
        self.username = "testuser"
        self.password = "test1234"
        self.email = "test@test.com"
        self.user = User.objects.create_user(username=self.username, password=self.password,
                                             email=self.email)
        self.diary = Diary.objects.create(author=self.user, date=datetime.datetime.now())
        self.token = Token.objects.get(user=self.user)

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_anonymous_user_try_see_list(self):
        """익명 유저가 diary list 에 접근할 때 테스트"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_authenticated_user_try_see_list(self):
        """로그인 한 유저가 diary list 에 접근할 때 테스트"""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_authenticated_user_try_see_list_with_token(self):
        """로그인 한 유저가 token 을 가지고 diary list 에 접근할 때 테스트"""
        self.client.login(username=self.username, password=self.password)
        self.api_authentication()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
