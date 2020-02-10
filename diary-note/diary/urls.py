from django.urls import path
from .views import DiaryList

app_name = 'diary'

urlpatterns = [
    path('list/', DiaryList.as_view(), name='diary_list'),
]
