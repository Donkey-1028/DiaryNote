import datetime
import json

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIRequestFactory

from .models import Diary
from .views import diary_list


class DiaryListTest(APITestCase):
    url = reverse('diary:diary_list')

    def setUp(self):
        """
        테스트 기본 설정
        """
        self.request_factory = APIRequestFactory()
        self.user = User.objects.create()
        Diary.objects.create(author_id=self.user.id, date=datetime.datetime.now())

    def test_diary_list_returns_correct_data(self):
        """
        해당 유저의 다이어리가 리턴되는지 테스트
        """
        request = self.request_factory.get(self.url)
        request.user = self.user
        response = diary_list(request)
        # APIRequestFactory()를 사용하여 직접 뷰를 테스트 하는 경우 내부의 요청-응답 사이클에 의해
        # 반한되는 response 는 rendering 된 데이터가 아니기 때문에 render 를 해줘야 한다고 함.
        response.render()  # html/text 가 application/json 으로 렌더링
        diary_decoded = response.content.decode()  # 가져온 바이트 코드 디코딩
        diary_json_loaded = json.loads(diary_decoded)  # json 디코딩
        print(diary_json_loaded)
        diary_owner = diary_json_loaded['diaries'][0]['author']

        self.assertEqual(diary_owner, self.user.id)
