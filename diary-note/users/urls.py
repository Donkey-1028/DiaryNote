from django.urls import path

from .views import UserRegistrationAPIView, UserLoginAPIView

app_name = 'users'

urlpatterns = [
    path('registration/', UserRegistrationAPIView.as_view(), name='registration'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
]
