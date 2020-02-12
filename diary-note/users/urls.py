from django.urls import path

from .views import UserRegistrationAPIView, UserLoginAPIView, UserTokenAPIView

app_name = 'users'

urlpatterns = [
    path('registration/', UserRegistrationAPIView.as_view(), name='registration'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('token/', UserTokenAPIView.as_view(), name='token'),
]
