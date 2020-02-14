from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from .models import Diary
from .serializer import DiaryListAPIViewSerializer, DiaryCreateAPIViewSerializer, DiaryRetrieveUpdateDestroyAPIViewSerializer


class DiaryListAPIView(ListAPIView):
    """Diary 전체 리스트 보기"""
    # authentication 은 해당하는 기능의 데이터에 접근할때 인증 방법인것 같다.
    # 세션인증 방식이라면 로그인이 되어있으면 되는것이고
    # 토큰 인증방식이라면 토큰을 인증했어야 된다.
    authentication_classes = (TokenAuthentication,)
    # permission 은 해당하는 기능에 접근할 수 있는 권한 인것 같다.
    permission_classes = (IsAuthenticated,)
    serializer_class = DiaryListAPIViewSerializer

    def get_queryset(self):
        queryset = Diary.objects.filter(author_id=self.request.user)
        return queryset


class DiaryCreateAPIView(CreateAPIView):
    """Diary 쓰기"""
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = DiaryCreateAPIViewSerializer

    def perform_create(self, serializer):
        """Diary 저장할 때 author 를 현재 로그인된 유저로 하기위해 오버라이딩"""
        serializer.save(author=self.request.user)


class DiaryRetrieveAPIView(RetrieveAPIView):
    """Diary 검색"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = DiaryRetrieveUpdateDestroyAPIViewSerializer

    def get_queryset(self):
        queryset = Diary.objects.filter(author=self.request.user)
        return queryset


class DiaryUpdateAPIView(UpdateAPIView):
    """Diary 수정"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = DiaryRetrieveUpdateDestroyAPIViewSerializer

    def get_queryset(self):
        queryset = Diary.objects.filter(author=self.request.user)
        return queryset


class DiaryDestroyAPIView(DestroyAPIView):
    """Diary 삭제"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = DiaryRetrieveUpdateDestroyAPIViewSerializer

    def get_queryset(self):
        queryset = Diary.objects.filter(author=self.request.user)
        return queryset
