from django.urls import path
from .views import DiaryListAPIView, DiaryCreateAPIView

app_name = 'diary'

urlpatterns = [
    path('list/', DiaryListAPIView.as_view(), name='diary_list'),
    path('create/', DiaryCreateAPIView.as_view(), name='diary_create'),
]
