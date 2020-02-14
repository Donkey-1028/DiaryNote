import datetime

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from .models import Diary


class DiaryCreateAPIViewTest(APITestCase):
    url = reverse('diary:diary_create')

    def setUp(self):
        self.username = "testuser"
        self.password = "test1234"
        self.email = "test@test.com"
        self.user = User.objects.create_user(username=self.username, password=self.password,
                                             email=self.email)

    def test_anonymous_user_try_create_new_diary(self):
        """익명 유저가 diary 를 create 할 때 테스트"""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

    def test_authenticated_user_try_create_new_diary_without_content(self):
        """로그인 된 유저가 diary 를 content data 없이 create 할 때 테스트"""
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 400)

    def test_authenticated_user_try_create_new_diary_with_wrong_date_data(self):
        """로그인 된 유저가 diary 를 잘못된 date data 로 create 할 때 테스트"""
        content = {
            "date": "wrong-date-data",
            "weather": "SY",
            "title": "title-test",
            "Contents": "contents-test",
            "realized": "realized-test"
        }
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(self.url, data=content)
        self.assertEqual(response.status_code, 400)

    def test_authenticated_user_try_create_new_diary_with_wrong_weather_data(self):
        """로그인 된 유저가 diary 를 잘못된 weather data 로 create 할 때 테스트"""
        content = {
            "date": "1995-10-28",
            "weather": "wrong-weather-data",
            "title": "title-test",
            "Contents": "contents-test",
            "realized": "realized-test"
        }
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(self.url, data=content)
        self.assertEqual(response.status_code, 400)

    def test_authenticated_user_try_create_new_diary_with_correct_content(self):
        """로그인 된 유저가 diary 를 정확한 content data 로 create 할 때 테스트"""
        content = {
            "date": "2020-02-15",
            "weather": "SY",
            "title": "title-test",
            "Contents": "contents-test",
            "realized": "realized-test"
        }
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(self.url, data=content)
        diary = Diary.objects.first()
        diary_count = Diary.objects.count()
        self.assertEqual(diary.author.username, self.username)
        self.assertEqual(diary_count, 1)
        self.assertEqual(response.status_code, 201)


class DiaryListAPIViewTest(APITestCase):
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
        """토큰 인증"""
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
