from django.urls import path

from .views import UserRegistrationAPIView

app_name = 'users'

urlpatterns = [
    path('registration/', UserRegistrationAPIView.as_view(), name='registration'),
]
