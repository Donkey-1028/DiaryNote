from django.urls import path
from .views import diary_list

app_name = 'diary'

urlpatterns = [
    path('list/', diary_list, name='diary_list'),
]
