import json
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
        diaries = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(diaries[0]['author'], self.user.id)

    def test_authenticated_user_try_see_list_without_create_list(self):
        """로그인 한 유저가 diary 를 create 하지 않고 diary list 에 접근할 때 테스트 """
        user2 = User.objects.create_user(username="testuser2", email="testuser2@test.com", password="test2345")
        user2_token = Token.objects.get(user=user2)
        self.client.login(username="testuser2", password="test2345")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user2_token.key)
        response = self.client.get(self.url)
        diaries = json.loads(response.content)
        self.assertEqual(len(diaries), 0)


class DiaryRetrieveAPIView(APITestCase):

    def setUp(self):
        self.username = "testuser"
        self.password = "test1234"
        self.email = "test@test.com"
        self.user = User.objects.create_user(username=self.username, password=self.password,
                                             email=self.email)
        self.token = Token.objects.get(user=self.user)
        self.diary = Diary.objects.create(author=self.user, date="2018-04-16", weather="SY")
        self.url = reverse('diary:diary_search', kwargs={'pk': self.diary.pk})

    def api_authentication(self):
        """토큰 인증"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_anonymous_user_try_search(self):
        """익명 유저가 diary 를 search 할 때 테스트"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_authenticated_user_try_search(self):
        """로그인 한 유저가 diary 를 search 할 때 테스트"""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_authenticated_user_try_search_with_token(self):
        """로그인 한 유저가 token 을 가지고 diary 를 search 할 때 테스트"""
        self.client.login(username=self.username, password=self.password)
        self.api_authentication()
        response = self.client.get(self.url)
        diary = Diary.objects.get(id=response.data['id'])
        self.assertEqual(response.data['id'], self.diary.pk)
        self.assertEqual(diary.author.username, self.username)
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_try_search_diary_without_create_diary(self):
        """로그인 한 유저가 diary 를 create 하지 않고 search 할 때 테스트"""
        user2 = User.objects.create_user(username="testuser2", email="testuser2@test.com", password="test2345")
        user2_token = Token.objects.get(user=user2)
        self.client.login(username="testuser2", password="test2345")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user2_token.key)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)


class DiaryUpdateAPIViewTest(APITestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "test1234"
        self.email = "test@test.com"
        self.user = User.objects.create_user(username=self.username, password=self.password,
                                             email=self.email)
        self.token = Token.objects.get(user=self.user)
        self.diary = Diary.objects.create(author=self.user, date="2018-04-16", weather="SY")
        self.url = reverse('diary:diary_update', kwargs={'pk': self.diary.pk})

    def api_authentication(self):
        """토큰 인증"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_anonymous_user_try_patch(self):
        """익명 유저가 patch 할 때 테스트"""
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, 401)

    def test_anonymous_user_try_put(self):
        """익명 유저가 put 할 때 테스트"""
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, 401)

    def test_authenticated_user_try_patch(self):
        """로그인 된 유저가 patch 할 때 테스트"""
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, 401)

    def test_authenticated_user_try_put(self):
        """로그인 된 유저가 put 할 때 테스트"""
        self.client.login(username=self.username, password=self.password)
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, 401)

    def test_authenticated_user_try_patch_with_token(self):
        """로그인 된 유저가 token 을 가지고 path 할 때 테스트"""
        self.client.login(username=self.username, password=self.password)
        self.api_authentication()
        patch_data = {
            "date": "2020-02-15",
            "weather": "FG",
            "title": "patch-test",
            "Contents": "patch-contents",
            "realized": "patch-realized"
        }
        response = self.client.patch(self.url, data=patch_data)
        patch_data['id'] = self.diary.pk
        self.assertEqual(response.status_code, 200)
        self.assertEqual(patch_data, response.data)

    def test_authenticated_user_try_put_with_token(self):
        """로그인 유저가 token 을 가지고 put 할 때 테스트"""
        self.client.login(username=self.username, password=self.password)
        self.api_authentication()
        put_data = {
            "date": "2020-02-15",
            "weather": "FG",
            "title": "patch-test",
            "Contents": "patch-contents",
            "realized": "patch-realized"
        }
        response = self.client.put(self.url, data=put_data)
        put_data['id'] = self.diary.pk
        self.assertEqual(response.status_code, 200)
        self.assertEqual(put_data, response.data)

    def test_authenticated_user_try_patch_and_put_with_wrong_data(self):
        """로그인 된 유저가 잘못된 데이터로 patch, put 할 때 테스트"""
        self.client.login(username=self.username, password=self.password)
        self.api_authentication()
        wrong_data = {
            "date": "wrong-date",
            "weather": "wrong-weather",
            "title": "patch-test",
            "Contents": "patch-contents",
            "realized": "patch-realized"
        }
        patch_response = self.client.patch(self.url, data=wrong_data)
        put_response = self.client.put(self.url, data=wrong_data)
        self.assertEqual(patch_response.status_code, put_response.status_code, 400)

    def test_authenticated_user_try_patch_and_put_without_create_diary(self):
        """로그인 한 유저가 diary 를 create 하지 않고 patch, put 할 때 테스트"""
        user2 = User.objects.create_user(username="testuser2", password="test2345", email="testuser2@test.com")
        user2_token = Token.objects.get(user=user2)
        self.client.login(username="testuser2", password="test2345")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user2_token.key)
        data = {
            "date": "2020-02-15",
            "weather": "FG",
            "title": "patch-test",
            "Contents": "patch-contents",
            "realized": "patch-realized"
        }
        patch_response = self.client.patch(self.url, data=data)
        put_response = self.client.put(self.url, data=data)
        self.assertEqual(patch_response.status_code, put_response.status_code, 404)
