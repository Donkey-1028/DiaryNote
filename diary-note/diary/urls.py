from django.urls import path
from .views import DiaryListAPIView, DiaryCreateAPIView, DiaryRetrieveAPIView, DiaryUpdateAPIView, DiaryDestroyAPIView

app_name = 'diary'

urlpatterns = [
    path('list/', DiaryListAPIView.as_view(), name='diary_list'),
    path('create/', DiaryCreateAPIView.as_view(), name='diary_create'),
    path('search/<pk>', DiaryRetrieveAPIView.as_view(), name='diary_search'),
    path('update/<pk>', DiaryUpdateAPIView.as_view(), name='diary_update'),
    path('delete/<pk>', DiaryDestroyAPIView.as_view(), name='diary_delete'),
]
